from datetime import datetime
from enum import Enum
from typing import Callable, Iterable

from typing_extensions import Self, Type

from models.base_model import BaseModel
from models.scheme import ValueOrm
from models.tag_model import TagModel


class ValueModel(BaseModel):

    def __init__(
            self,
            type_: Enum = None,
            message: str = None,
            price_usd: float = None,
            price_gel: float = None,
            date_: datetime = None,
            orm: ValueOrm = None
    ) -> None:
        if orm:
            self.orm = orm
        else:
            self.orm = ValueOrm(type=type_, message=message, price_usd=price_usd, price_gel=price_gel, date=date_)

    def __str__(self) -> str:
        return "Value id: {id}, type: {type}, price_usd: {usd}, price_gel: {gel}, date: {date}".format(
                id=self.orm.id, type=self.orm.type, usd=self.orm.price_usd,
                gel=self.orm.price_gel, date=self.orm.date
                )

    def __repr__(self) -> str:
        return "<ValueModel(id={id}, type_={type}, message='{msg}', price_usd={usd}, price_gel={gel}, date={date})>|" \
               "<ValueModel(orm='{orm}')>".format(
                id=self.orm.id, type=self.orm.type, msg=self.orm.message,
                usd=self.orm.price_usd, gel=self.orm.price_gel, date=self.orm.date, orm=self.orm
                )

    def add_tags(self, tags: list[TagModel]) -> int:
        count = 0
        self.delete_all_tags()
        for tag in tags:
            self.orm.tags.append(tag.get())
            count += 1
        if count > 0:
            self.save()
        return count

    def remove_tags(self, tags: list[TagModel]) -> int:
        count = 0
        for tag in tags:
            self.orm.tags.remove(tag.get())
            count += 1
        if count > 0:
            self.save()
        return count

    def delete_all_tags(self) -> None:
        self.orm.tags = []
        self.save()

    @staticmethod
    def get_one(iid: int) -> Self | None:
        orm = ValueOrm.get_one(iid=iid)
        if orm:
            return ValueModel(orm=orm)

    @staticmethod
    def get_all(filter_: dict[str, int | str] = None, order_: dict[str, Callable] = None) -> list[Self]:
        tags = ValueOrm.get_all(filter_, order_)
        return [ValueModel(orm=orm) for orm in tags]
