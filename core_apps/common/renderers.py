import json
from typing import Optional, Any, Union
from django.utils.translation import gettext_lazy as _
from rest_framework.renderers import JSONRenderer


class GenericJSONRenderer(JSONRenderer):
    charset = "utf-8"
    object_label = "object"

    def render(
        self,
        data: Any,
        accepted_media_type: Optional[str] = None,
        renderer_context: Optional[dict] = None,
    ) -> Union[bytes, str]:
        if renderer_context is None:
            renderer_context = {}

        view = renderer_context.get("view")
        object_label = getattr(view, "object_label", self.object_label)

        response = renderer_context.get("response")
        if not response:
            raise ValueError(_("Response not found in renderer context"))

        status_code = response.status_code

        #Errors = (4xx ,5xx):
        if status_code >= 400:
            return super().render(data, accepted_media_type, renderer_context)

        # Wrap the response
        response_data = {
            "status_code": status_code,
            "object_label": object_label,
            "data": data,
        }

        return super().render(response_data, accepted_media_type, renderer_context)

