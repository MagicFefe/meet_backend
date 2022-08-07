from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette import status
from custom_route.admin_check_route import AdminRightsRoute
from di.application_container import ApplicationContainer
from models.feedback.feedback_add import FeedbackAdd
from models.feedback.feedback_response import FeedbackResponse
from repositories.feedback_repository import FeedbackRepository, from_feedback_to_feedback_response

router = APIRouter(
    prefix="/api/feedback",
    tags=["feedback"],
    route_class=AdminRightsRoute
)


@router.post(
    path="",
)
@inject
async def send_feedback(
        new_feedback: FeedbackAdd,
        feedback_repository: FeedbackRepository = Depends(
            Provide[ApplicationContainer.repository_container.feedback_repository]
        )
):
    await feedback_repository.add_feedback(new_feedback)
    return status.HTTP_200_OK


@router.get(
    path="/all",
    response_model=list[FeedbackResponse]
)
@inject
async def get_all_feedbacks(
        feedback_repository: FeedbackRepository = Depends(
            Provide[ApplicationContainer.repository_container.feedback_repository]
        )
):
    feedbacks = await feedback_repository.get_all_feedbacks()
    feedback_response_list: list[FeedbackResponse] = []
    for feedback in feedbacks:
        feedback_response_list.append(from_feedback_to_feedback_response(feedback))
    return feedback_response_list
