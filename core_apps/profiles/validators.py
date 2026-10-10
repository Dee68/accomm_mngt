from django.core.exceptions import ValidationError

MAX_AVATAR_SIZE = 2 * 1024 * 1024
ALLOWED_AVATAR_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}

def validate_avatar_size(image):
    if image.size > MAX_AVATAR_SIZE:
        raise ValidationError(
            f"Avatar must be smaller than {MAX_AVATAR_SIZE // (1024 * 1024)} MB."
        )

def validate_avatar_extension(image):
    ext = image.name.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_AVATAR_EXTENSIONS:
        raise ValidationError(
            f"Unsupported format. Allowed: {', '.join(sorted(ALLOWED_AVATAR_EXTENSIONS))}."
        )