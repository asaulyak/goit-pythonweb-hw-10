from datetime import datetime, timedelta
from sqlalchemy import select, extract, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.contacts_model import Contact
from src.features.contacts.schema.contact_schema import ContactModel
from src.features.contacts.schema.contact_update_schema import ContactUpdateModel


class ContactsRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_contacts(self, skip: int, limit: int):
        stmt = select(Contact).offset(skip).limit(limit)
        contacts = await self.db.execute(stmt)

        return contacts.scalars().all()

    async def get_contact_by_id(self, contact_id: int) -> Contact | None:
        stmt = select(Contact).filter_by(id=contact_id)
        contact = await self.db.execute(stmt)

        return contact.scalar_one_or_none()

    async def search_contact(
        self, first_name: str | None, last_name: str | None, email: str | None
    ):
        stmt = select(Contact)

        if first_name:
            stmt = stmt.filter_by(first_name=first_name)

        if last_name:
            stmt = stmt.filter_by(last_name=last_name)

        if email:
            stmt = stmt.filter_by(email=email)

        contacts = await self.db.execute(stmt)

        return contacts.scalars().all()

    async def get_contact_by_email(self, contact_email: str) -> Contact | None:
        stmt = select(Contact).filter_by(email=contact_email)
        contact = await self.db.execute(stmt)

        return contact.scalar_one_or_none()

    async def create_contact(self, body: ContactModel) -> Contact:
        contact = Contact(**body.model_dump(exclude_unset=True))
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)

        return await self.get_contact_by_id(contact.id)

    async def update_contact(
        self, contact_id: int, body: ContactUpdateModel
    ) -> Contact | None:
        contact = await self.get_contact_by_id(contact_id)

        if not contact:
            return None

        if body.first_name:
            contact.first_name = body.first_name

        if body.last_name:
            contact.last_name = body.last_name

        if body.birth_day:
            contact.birth_day = body.birth_day

        if body.phone:
            contact.phone = body.phone

        if body.data:
            contact.data = body.data

        await self.db.commit()
        await self.db.refresh(contact)

        return contact

    async def delete_contact(self, contact_id: int) -> Contact | None:
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()

        return contact

    async def bd_soon(self, days: int) -> list[Contact]:
        today = datetime.now().date()
        end_date = today + timedelta(days=days)

        stmt = select(Contact).where(
            or_(
                # Case 1: Birthday within the same month
                (extract("month", Contact.birth_day) == today.month)
                & (extract("day", Contact.birth_day) >= today.day)
                & (extract("day", Contact.birth_day) <= end_date.day),
                # Case 2: Birthday in the next month
                (extract("month", Contact.birth_day) == end_date.month)
                & (extract("day", Contact.birth_day) <= end_date.day)
                & (today.month != end_date.month),
            )
        )

        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()
