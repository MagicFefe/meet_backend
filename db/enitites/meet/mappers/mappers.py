from db.enitites.meet.meet_db import MeetDB
from models.meet.meet_response import MeetResponse


def from_meet_db_to_meet_response(meet_db: MeetDB) -> MeetResponse:
    return MeetResponse(
        id=meet_db.id,
        author_id=meet_db.author_id,
        meet_name=meet_db.meet_name,
        meet_description=meet_db.meet_description,
        latitude=meet_db.latitude,
        longitude=meet_db.longitude,
        created_at=meet_db.created_at
    )
