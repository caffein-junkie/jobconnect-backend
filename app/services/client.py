from typing import List
from app.schemas.client import ClientInDB, ClientResponse, ClientUpdate, ClientCreate
from app.repositories.client import ClientRepository
from app.utils.security import SecurityUtils
from app.utils.exceptions import (
    NotFoundException,
    InvalidCredentialsException
)


class ClientService:

    def __init__(self, repo: ClientRepository) -> None:
        self.repo = repo

    @staticmethod
    def client_in_db_to_response(client: ClientInDB) -> ClientResponse:
        """"""
        return ClientResponse(
            name=client.name,
            surname=client.surname,
            email=client.email,
            phone_number=client.phone_number,
            location_name=client.location_name,
            longitude=client.longitude,
            latitude=client.latitude,
            client_id=client.client_id,
            created_at=client.created_at
        )
    
    async def create_client(self, client_data: ClientCreate) -> ClientResponse:
        """"""
        client = await self.repo.create(client_data)
        return ClientService.client_in_db_to_response(client)
    
    async def get_all_clients(self) -> List[ClientResponse]:
        clients = await self.repo.get_all()
        return [ClientService.client_in_db_to_response(c) for c in clients]
    
    async def get_client(self, client_id: str) -> ClientResponse:
        """"""
        client = await self.repo.get_by_id(client_id)
        if not client: raise NotFoundException(f"Client with id '{client_id}' not found")
        return ClientService.client_in_db_to_response(client)
    
    async def update_client(
        self,
        client_id: str,
        update_data: ClientUpdate,
        ) -> ClientResponse:
        """"""
        updated_client = await self.repo.update(client_id, update_data)
        if not updated_client: raise  NotFoundException(f"Client with id '{client_id}' not found")
        return ClientService.client_in_db_to_response(updated_client)
    
    async def delete_client(self, client_id: str) -> None:
        """"""
        await self.repo.delete(client_id)

    async def authenticate_client_with_email_and_password(self, email: str, password: str) -> ClientResponse:
        """"""
        raise NotImplementedError("authentication has not been implemented yet")
        # client = await self.repo.get_by_email(email)
        # if not client:
        #     raise InvalidCredentialsException()
        # if not SecurityUtils.verify_password(password, client.password_hash):
        #     raise InvalidCredentialsException()
        # return ClientService.client_in_db_to_response(client)
