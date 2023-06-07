import calendar
import datetime as dt
import helper as hlp


from enum import Enum
from typing import Callable, Iterable

from sqlalchemy import desc, and_
from typing_extensions import Self, Type

from lang_pack.lang import LANG_GENERAL
from logger.logger import log
from models.base_model import BaseModel
from models.scheme import ValueOrm, TypeEnum
from models.tag_model import TagModel


class ValueModel(BaseModel):

    LATEST_VALUES = 30

    def __init__(
            self,
            type: Enum = None,
            message: str = None,
            price_usd: float = None,
            price_gel: float = None,
            date: dt.datetime = None,
            orm: ValueOrm = None
    ) -> None:
        if orm:
            self.orm = orm
        else:
            self.orm = ValueOrm(type=type, message=message, price_usd=price_usd, price_gel=price_gel, date=date)

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
            self.orm.tags.append(tag)
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
    def get_by_id(iid: int) -> Self | None:
        orm = ValueOrm.get_one({'id': iid})
        if orm:
            return ValueModel(orm=orm)

    @staticmethod
    def get_latest() -> list[Self]:
        values = ValueOrm.get_all(order_={'date': desc, 'id': desc}, limit=ValueModel.LATEST_VALUES)
        return [ValueModel(orm=orm) for orm in values]

    @staticmethod
    def get_all_filtered(date_from: tuple, date_to: tuple, tags: list):
        start_date, end_date = hlp.prepare_filter_dates(date_from, date_to)
        values = ValueOrm.get_all(
            filter_=[ValueOrm.date <= start_date, ValueOrm.date >= end_date],
            order_={'date': desc, 'id': desc},
            tags=tags
        )
        return [ValueModel(orm=orm) for orm in values]

    @staticmethod
    def date_formated(dt):
        return dt.strftime('%d %B, %Y')

    def display_price(self, price):
        if not price:
            return ''
        price = "{:.2f}".format(price)
        if self.orm.type == TypeEnum.VOUT:
            return f"-{price}"
        return price

    @staticmethod
    def get_years_range():
        years = ValueOrm.get_years_range()
        if years:
            years = [y[0] for y in years]
        return years


