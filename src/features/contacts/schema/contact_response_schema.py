import datetime

from pydantic import ConfigDict

from src.features.contacts.schema.contact_schema import ContactModel


class ContactResponseModel(ContactModel):
    id: int
    model_config = ConfigDict(from_attributes=True, json_encoders={datetime.datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")}
)
