import logging
from django.conf import settings
from typing import Optional
from djoser.social.views import ProviderAuthView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

logger = logging.getLogger(__name__)

# helper function to get cookies
def set_auth_cookies(response: Response, access_token: str, refresh_token: Optional[str] = None) -> None:
    access_token_lifetime = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
    refresh_token_lifetime = settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()

    # Common cookie settings
    cookie_settings = {
        "path": settings.COOKIE_PATH,
        "secure": settings.COOKIE_SECURE,
        "httponly": settings.COOKIE_HTTPONLY,
        "samesite": settings.COOKIE_SAMESITE,
    }
    
    # Set Access Token Cookie
    response.set_cookie("access", access_token, max_age=access_token_lifetime, **cookie_settings)

    # Set Refresh Token Cookie (Only if Provided)
    if refresh_token:
        refresh_cookie_settings = cookie_settings.copy()
        refresh_cookie_settings["max_age"] = refresh_token_lifetime

        response.delete_cookie("refresh")  # Ensure old refresh token is removed
        response.set_cookie("refresh", refresh_token, **refresh_cookie_settings)

    # 🔹 Set Logged-in Status Cookie (Non-HttpOnly, for Frontend Visibility)
    logged_in_cookie_settings = cookie_settings.copy()
    logged_in_cookie_settings["httponly"] = False  # Allow frontend access
    response.set_cookie("logged_in", "true", **logged_in_cookie_settings)



class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        logger.info(f"Incoming request cookies: {request.COOKIES}")

        # Get refresh token from cookies
        refresh_token = request.COOKIES.get("refresh") or request.data.get("refresh")
        logger.info(f"Extracted refresh token: {refresh_token}")

        if not refresh_token:
            return Response({"error": "No refresh token provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a new request object with the refresh token in `data`
        request_data = {"refresh": refresh_token}
        new_request = request._request
        new_request.data = request_data 

        

        # Call parent method with modified request data
        try:
            refresh_res = super().post(new_request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error refreshing token: {e}", exc_info=True)
            return Response({"error": "Token refresh failed", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        logger.info(f"Refresh response status: {refresh_res.status_code}")
        logger.info(f"Refresh response data: {refresh_res.data}")

        if refresh_res.status_code == status.HTTP_200_OK:
            access_token = refresh_res.data.get("access")
            new_refresh_token = refresh_res.data.get("refresh")

            if access_token and new_refresh_token:
                set_auth_cookies(refresh_res, access_token=access_token, refresh_token=new_refresh_token)
                refresh_res.data.pop("access", None)
                refresh_res.data.pop("refresh", None)
                refresh_res.data["message"] = "Access tokens refreshed successfully."
            else:
                logger.error("Access or Refresh token missing in refresh response.")
                refresh_res.data["message"] = "Token refresh failed."

        return refresh_res





class CustomProviderAuthView(ProviderAuthView):
    def post(self,request:Request,*args,**kwargs)->Response:
        provider_res = super().post(request,**args, **kwargs)
        if provider_res.status_code == status.HTTP_201_CREATED:
            access_token = provider_res.data.get("access")
            refresh_token = provider_res.data.get("refresh")
            if access_token and refresh_token:
                set_auth_cookies(provider_res,access_token=access_token,refresh_token=refresh_token)
                provider_res.data.pop("access",None)
                provider_res.data.pop("refresh",None)
                provider_res.data["message"] = "You are logged in Successful."
            else:
                provider_res.data["message"] = "Access or Refresh token not found in provider response."
                logging.error("Access or Refresh token not found in provider response data.")
        return provider_res
    


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        logger.info(f"Login request received: {request.data}")  # Log request data

        token_res = super().post(request, *args, **kwargs)

        logger.info(f"Login response status: {token_res.status_code}")
        logger.info(f"Login response data before processing: {token_res.data}")  # Log response data

        if token_res.status_code == status.HTTP_200_OK:
            access_token = token_res.data.get("access")
            refresh_token = token_res.data.get("refresh")

            if access_token and refresh_token:
                # Securely set cookies
                set_auth_cookies(token_res, access_token=access_token, refresh_token=refresh_token)

                # Remove tokens from response body for security
                token_res.data.pop("access", None)
                token_res.data.pop("refresh", None)
                token_res.data["message"] = "Login Successful."
            else:
                logger.error("Access or Refresh token missing in login response.")
                token_res.data["message"] = "Login Failed: Token generation error."
        
        return token_res

class LogoutAPIView(APIView):
    def post(self,request:Request,*args,**kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        response.delete_cookie("logged_in")
        return response