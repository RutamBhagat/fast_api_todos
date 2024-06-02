from sqlalchemy.orm.session import Session
from app.db.models import DBAddresses, DBUsers
from app.db.schema import AddressBody


# create a new address
async def create_address(
    db: Session, address: AddressBody, user: DBUsers
) -> DBAddresses:
    # delete the old address
    old_address = (
        db.query(DBAddresses).filter(DBAddresses.id == user.address_id).first()
    )
    if old_address is not None:
        db.delete(old_address)

    address = DBAddresses(**address.model_dump())
    db.add(address)
    db.flush()
    user.address_id = address.id
    db.add(user)
    db.commit()
    db.refresh(address)
    return address
