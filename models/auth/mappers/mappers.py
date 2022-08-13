from base64 import b64encode
from config import USER_IMAGE_PLACEHOLDER_PATH, ENCODING
from db.enitites.user.user import User
from files.file_manager import FileManager
from models.auth.sign_up import SignUp
from utils.password_utils import get_hashed_password


async def from_sign_up_to_user(
        sign_up: SignUp,
        user_image_file_manager: FileManager
) -> User:
    image_file_name = f"{sign_up.email}.txt"
    user = User()
    user.name = sign_up.name
    user.surname = sign_up.surname
    user.dob = sign_up.dob
    user.gender = sign_up.gender
    user.about = sign_up.about
    user.email = sign_up.email
    user.city = sign_up.city
    user.country = sign_up.country
    user.password = get_hashed_password(sign_up.password, sign_up.email)
    if sign_up.image is None:
        with open(USER_IMAGE_PLACEHOLDER_PATH, "rb") as image_file:
            image = b64encode(image_file.read()).decode(ENCODING)
        user.image_filename = await user_image_file_manager.write_or_create_file(image_file_name, image)
    else:
        image = sign_up.image
        user.image_filename = await user_image_file_manager.write_or_create_file(image_file_name, image)
    return user
