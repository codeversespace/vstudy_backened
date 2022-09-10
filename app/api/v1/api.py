# app/api/api_v1/api.py
from fastapi import APIRouter

from app.api.v1.endpoints import bulkupload ,users,level,quiz,questions,answer,category,subject

api_router = APIRouter()
api_router.include_router(bulkupload.router,  prefix="/action/bulk", tags=["Bulk Operation"])
api_router.include_router(users.router, tags=["users"])
api_router.include_router(level.router, tags=["level"])
api_router.include_router(quiz.router, tags=["quiz"])
api_router.include_router(questions.router, tags=["questions"])
api_router.include_router(answer.router, tags=["answer"])
api_router.include_router(category.router, tags=["category"])
api_router.include_router(subject.router, tags=["subject"])