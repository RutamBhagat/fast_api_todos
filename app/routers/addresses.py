from fastapi import APIRouter, status
from app.models import Addresses
from app.routers.utils.utility_funcs import user_dependency, db_dependency
from app.routers.utils.type_classes import Address_Request


router = APIRouter(prefix="/addresses", tags=["addresses"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_address(
    db: db_dependency,
    user: user_dependency,
    address_request: Address_Request,
):
    new_address = Addresses(
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
