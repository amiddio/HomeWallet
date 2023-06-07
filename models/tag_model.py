from typing import Callable
from sqlalchemy import asc
from typing_extensions import Self
from models.base_model import BaseModel
from models.scheme import TagOrm


class TagModel(BaseModel):

    def __init__(self, name: str = None, orm: TagOrm = None) -> None:
        if orm:
            self.orm = orm
        else:
            self.orm = TagOrm(name=name)

    def __str__(self) -> str:
        return "Tag id: {id}, name: '{name}'".format(id=self.orm.id, name=self.orm.name)

    def __repr__(self):
        return "<TagModel(name='{name}')>|<TagModel(orm='{orm}')>".format(name=self.orm.name, orm=self.orm)

    @staticmethod
    def is_exist(name: str) -> Self:
        orm = TagOrm.get_one({'name': name})
        if orm:
            return TagModel(orm=orm)

    @staticmethod
    def get_by_id(iid: int) -> Self | None:
        orm = TagOrm.get_one({'id': iid})
        if orm:
            return TagModel(orm=orm)

    @staticmethod
    def get_all(filter_: dict[str, int | str] = None, order_: dict[str, Callable] = None) -> list[Self]:
        tags = TagOrm.get_all(filter_, order_)
        return [TagModel(orm=orm) for orm in tags]

    @staticmethod
    def get_checked_tags(selected: list[int]):
        result = []
        if not selected:
            return result
        for i, tag in zip(selected, TagModel.get_all(order_={'name': asc})):
            if i.get() > 0:
                result.append(tag.get())
        return result


