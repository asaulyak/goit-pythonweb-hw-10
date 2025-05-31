from typing import Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.features.contacts.contacts_service import ContactsService
from src.features.contacts.schema.contact_response_schema import ContactResponseModel
from src.features.contacts.schema.contact_schema import ContactModel
from src.features.contacts.schema.contact_update_schema import ContactUpdateModel

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=list[ContactResponseModel])
async def get_contacts(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    contacts_service = ContactsService(db)
    contacts = await contacts_service.get_contacts(skip, limit)

    return contacts


@router.get("/search", response_model=list[ContactResponseModel])
async def search(
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    contacts_service = ContactsService(db)

    return await contacts_service.search(first_name, last_name, email)


@router.get("/soon_celebrate", response_model=list[ContactResponseModel])
async def search(db: AsyncSession = Depends(get_db)):
    contacts_service = ContactsService(db)

    return await contacts_service.soon_celebrate()


@router.post(
    "/", response_model=ContactResponseModel, status_code=status.HTTP_201_CREATED
)
async def create_contact(body: ContactModel, db: AsyncSession = Depends(get_db)):
    contacts_service = ContactsService(db)

    return await contacts_service.create_contact(body)


@router.get("/{contact_id}", response_model=ContactResponseModel)
async def get_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contacts_service = ContactsService(db)
    return await contacts_service.get_contact_by_id(contact_id)


@router.patch(
    "/{contact_id}",
    response_model=ContactResponseModel,
    status_code=status.HTTP_201_CREATED,
)
async def create_contact(
    contact_id: int, body: ContactUpdateModel, db: AsyncSession = Depends(get_db)
):
    contacts_service = ContactsService(db)

    return await contacts_service.update_contact(contact_id, body)


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contacts_service = ContactsService(db)

    await contacts_service.delete_contact(contact_id)
