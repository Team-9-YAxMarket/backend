from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core import exceptions
from src.db.db import get_session
from src.db.models import Item
from src.repository.abstract_repository import AbstractRepository


@dataclass
class ItemDTO:
    id: UUID
    count: int
    sku: str
    barcode: str
    img: str


class ItemRepository(AbstractRepository):
    """Репозиторий для работы с моделью Item."""

    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        super().__init__(session, Item)

    async def get_by_order_and_sku(self, order_id: UUID, sku: str) -> Item:
        """Return item by order id and sku. Raise exception if not found."""
        stmt = (
            select(Item)
            .options(selectinload(Item.prompts))
            .where(
                Item.order_id == order_id,
                Item.sku == sku,
            )
        )
        item = (await self._session.execute(stmt)).scalars().first()

        if not item:
            raise exceptions.ObjectNotFoundError(Item)

        return item

    async def get_all_items(self) -> List[Optional[Item]]:
        stmt = select(Item).options(
            selectinload(Item.prompts),
        )
        items = await self._session.execute(stmt)
        return items.scalars().all()
