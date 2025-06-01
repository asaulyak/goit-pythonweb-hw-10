from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.auth.contacts_repository import ContactsRepository
from src.auth.hash import Hash, create_access_token
from src.features.auth.schema.login_schema import LoginModel


class LoginService:
    def __init__(self, db: AsyncSession):
        self.contacts_repository = ContactsRepository(db)

    async def login(self, schema: LoginModel):
        contact = await self.contacts_repository.get_contact_by_email(schema.email)

        if not contact:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password",
            )

        verified = Hash().verify_password(schema.password, contact.password)

        if not verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password",
            )

        access_token = await create_access_token({"sub": contact.email})

        return {"access_token": access_token, "token_type": "bearer"}
