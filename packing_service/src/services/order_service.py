from typing import List

from fastapi import Depends

from src.api.request_models.order_request import OrderCreateRequest
from src.db.models import Order
from src.repository.order_repository import OrderRepository
from src.services.item_service import ItemService


class OrderService:
    def __init__(
        self,
        order_repository: OrderRepository = Depends(),
        item_service: ItemService = Depends(),
    ) -> None:
        self._order_repository = order_repository
        self._item_service = item_service

    async def list_all_orders(self) -> List[Order]:
        return await self._order_repository.get_all()

    async def get_next_order(self) -> Order:
        return await self._order_repository.get_next_forming_order()

    async def create_order(self, schema: OrderCreateRequest) -> Order:
        items = [await self._item_service.create_item(i) for i in schema.items]
        order = Order(items=items)
        return await self._order_repository.create(order)
