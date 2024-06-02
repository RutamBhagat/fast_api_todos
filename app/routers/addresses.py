from fastapi import APIRouter, status
from app.db.models import DBAddresses
from app.db.schema import AddressBody
from app.dependencies import user_dependency, db_dependency


router = APIRouter(prefix="/addresses", tags=["addresses"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_address(
    db: db_dependency,
    user: user_dependency,
    address_request: AddressBody,
):
    new_address = DBAddresses(
        address1=address_request.address1,
        address2=address_request.address2,
        city=address_request.city,
        state=address_request.state,
        country=address_request.country,
        postalcode=address_request.postalcode,
    )
    db.add(new_address)
    db.flush()
    user.address_id = new_address.id
    db.add(user)
    db.commit()
