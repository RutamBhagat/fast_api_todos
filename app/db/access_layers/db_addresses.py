from sqlalchemy.orm.session import Session
from app.db.models import DBAddresses, DBUsers
from app.db.schema import AddressBody


# create a new address and upate the user's address_id
async def create_address(db: Session, address_request: AddressBody, user: DBUsers):
    address = DBAddresses(**address_request.model_dump())
    db.add(address)
    db.commit()
    user.address_id = address.id
    db.commit()
