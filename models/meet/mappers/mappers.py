from datetime import datetime
from uuid import uuid4
from db.enitites.meet.meet_db import MeetDB
from db.enitites.user.user import User
from files.file_manager import FileManager
from models.meet.meet import Meet
from models.meet.meet_response import MeetResponse
from models.meet.meet_response_details import MeetResponseDetails


async def from_meet_response_to_meet_response_details(
        meet: MeetResponse,
        user: User,
        image_file_manager: FileManager
) -> MeetResponseDetails:
    user_image = await image_file_manager.read_file(user.image_filename)
    return MeetResponseDetails(
        id=meet.id,
        author_id=meet.author_id,
        author_name=user.name,
        author_surname=user.surname,
        author_image=user_image,
        meet_name=meet.meet_name,
        meet_description=meet.meet_description,
        latitude=meet.latitude,
        longitude=meet.longitude,
        created_at=meet.created_at
    )


def from_meet_to_meet_db(meet: Meet) -> MeetDB:
    meet_id = str(uuid4())
    date = str(datetime.now())
    meet_db = MeetDB(
        id=meet_id,
        meet_description=meet.meet_description,
        meet_name=meet.meet_name,
        author_name=meet.author_name,
        author_surname=meet.author_surname,
        author_id=meet.author_id,
        latitude=meet.latitude,
        longitude=meet.longitude,
        created_at=date
    )
    return meet_db
