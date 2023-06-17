from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.api.dto.order_dto import OrderDTO
from src.db.db import get_session
from src.db.models import Item, Order, RecommendedCarton
from src.repository.abstract_repository import AbstractRepository


class OrderRepository(AbstractRepository):
    """Репозиторий для работы с моделью Order."""

    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        super().__init__(session, Order)

    async def get_full_order_by_id(self, order_id: UUID) -> Optional[Order]:
        stmt = (
            select(Order)
            .options(
                selectinload(Order.items).selectinload(Item.prompts),
                selectinload(Order.recommended_carton),
                selectinload(Order.selected_carton),
            )
            .where(Order.id == order_id)
        )
        return (await self._session.execute(stmt)).scalars().first()

    async def get_next_forming_order(self) -> Optional[OrderDTO]:
        stmt = (
            select(Order)
            .options(
                selectinload(Order.items).selectinload(Item.prompts),
                selectinload(Order.recommended_carton).selectinload(
                    RecommendedCarton.carton
                ),
                selectinload(Order.selected_carton),
            )
            .where(Order.status == Order.OrderStatus.IS_FORMING)
            .order_by(Order.updated_at)
        )
        order = (await self._session.execute(stmt)).scalars().first()
        if not order:
            return None
        return OrderDTO.parse_from_db(order)

    async def get_order_by_name_or_none(self, order: str) -> Optional[Order]:
        order = await self._session.execute(
            select(Order).where(Order.order == order)
        )
        return order.scalars().first()
