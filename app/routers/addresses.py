from fastapi import APIRouter, status
from app.db.schema import AddressBody
from app.db.access_layers import db_addresses
from app.dependencies import user_dependency, db_dependency


router = APIRouter(prefix="/addresses", tags=["addresses"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AddressBody)
async def create_address(
    db: db_dependency,
    user: user_dependency,
    address_request: AddressBody,
):
    await db_addresses.create_address(db, address_request, user)
    return address_request
