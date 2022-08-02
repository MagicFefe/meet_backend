from PIL import Image
from io import BytesIO
from base64 import b64decode
from config import MIN_USER_IMAGE_WIDTH_PX, MIN_USER_IMAGE_HEIGHT_PX, MAX_USER_IMAGE_WIDTH_PX, MAX_USER_IMAGE_HEIGHT_PX
from exceptions import InvalidImageError


def validate_image(image: str):
    try:
        decoded_image = Image.open(BytesIO(b64decode(image)))
    except Exception:
        raise InvalidImageError(detail="image_filename must be jpeg or png format")
    width, height = decoded_image.size
    if width != height:
        raise InvalidImageError(detail="image_filename must be a square")
    if width < MIN_USER_IMAGE_WIDTH_PX or height < MIN_USER_IMAGE_HEIGHT_PX:
        raise InvalidImageError(detail="image_filename is too small")
    if width > MAX_USER_IMAGE_WIDTH_PX or height > MAX_USER_IMAGE_HEIGHT_PX:
        raise InvalidImageError(detail="image_filename is to large")
