from db.enitites.user.user import User
from files.file_manager import FileManager
from models.user.user_response import UserResponse, UserResponseWithToken
from utils.jwt_utils import generate_jwt


def from_user_to_user_response_with_token(
        user: User,
        user_image_file_manager: FileManager
):
    jwt = generate_jwt(
        {
            "name": user.name,
            "surname": user.surname,
            "email": user.email
        }
    )
    user_response = UserResponseWithToken(
        id=str(user.id),
        name=user.name,
        surname=user.surname,
        about=user.about,
        dob=user.dob,
        gender=user.gender,
        email=user.email,
        country=user.country,
        city=user.city,
        jwt=str(jwt),
        image=user_image_file_manager.read_file(user.image_filename)
    )
    return user_response


def from_user_to_user_response(
        user: User,
        user_image_file_manager: FileManager
):
    user_response = UserResponse(
        id=str(user.id),
        name=user.name,
        surname=user.surname,
        about=user.about,
        dob=user.dob,
        gender=user.gender,
        email=user.email,
        country=user.country,
        city=user.city,
        image=user_image_file_manager.read_file(user.image_filename)
    )
    return user_response
