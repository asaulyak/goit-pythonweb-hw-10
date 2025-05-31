from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.features.contacts.contacts_repository import ContactsRepository
from src.features.contacts.schema.contact_schema import ContactModel
from src.features.contacts.schema.contact_update_schema import ContactUpdateModel


class ContactsService:
    def __init__(self, db: AsyncSession):
        self.contacts_repository = ContactsRepository(db)

    async def get_contacts(self, skip: int, limit: int):
        return await self.contacts_repository.get_contacts(skip, limit)

    async def get_contact_by_id(self, contact_id: int):
        contact = await self.contacts_repository.get_contact_by_id(contact_id)

        if not contact:
            raise HTTPException(
                detail="Contact not found", status_code=status.HTTP_404_NOT_FOUND
            )

        return contact

    async def create_contact(self, body: ContactModel):
        existing_contact = await self.contacts_repository.get_contact_by_email(
            body.email
        )

        if existing_contact:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Contact already exists"
            )

        return await self.contacts_repository.create_contact(body)

    async def update_contact(self, contact_id: int, body: ContactUpdateModel):
        return await self.contacts_repository.update_contact(contact_id, body)

    async def delete_contact(self, contact_id: int):
        return await self.contacts_repository.delete_contact(contact_id)

    async def search(
        self, first_name: str | None, last_name: str | None, email: str | None
    ):
        if not first_name and not last_name and not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No search parameters provided",
            )

        return await self.contacts_repository.search_contact(
            first_name, last_name, email
        )

    async def soon_celebrate(self, days: int = 7):
        return await self.contacts_repository.bd_soon(days)
