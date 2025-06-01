from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.features.auth.login_service import LoginService
from src.features.auth.schema.auth_response_schema import AuthResponseModel
from src.features.auth.schema.login_schema import LoginModel

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=AuthResponseModel)
async def login(body: LoginModel, db: AsyncSession = Depends(get_db)):
    login_service = LoginService(db)

    return await login_service.login(body)
