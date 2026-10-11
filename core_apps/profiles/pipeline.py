import logging
import cloudinary.uploader
from core_apps.profiles.models import Profile

logger = logging.getLogger(__name__)


def save_profile(backend, user, response, *args, **kwargs):
    """
    Pipeline step: after a successful social login, fetch the user's
    Google profile picture and upload it to Cloudinary, then save it
    on their Profile.
    """
    if backend.name != "google-oauth2":
        return

    # `response` here is the raw userinfo dict from Google's OpenID endpoint.
    # The key names depend on the scope and the social_core backend version.
    avatar_url = response.get("picture")
    if not avatar_url:
        logger.info("No picture in Google response for user %s", user.username)
        return

    profile, _ = Profile.objects.get_or_create(user=user)

    # Only upload if the user has no avatar yet, or if you want to refresh it
    # on every login, drop this check.
    if profile.avatar:
        logger.info("User %s already has an avatar; skipping", user.username)
        return

    try:
        upload_result = cloudinary.uploader.upload(
            avatar_url,
            folder="avatars",
            resource_type="image",
        )
    except Exception as exc:
        logger.exception("Cloudinary upload failed for %s: %s", user.username, exc)
        return

    profile.avatar = upload_result["secure_url"]
    profile.save(update_fields=["avatar"])
    logger.info("Saved avatar for %s", user.username)