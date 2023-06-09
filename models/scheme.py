import enum

from typing import Callable, Any
from sqlalchemy import (
    create_engine, and_, func, Column, Integer, String, Float, DateTime, Enum, Table, ForeignKey, extract, desc
)
from sqlalchemy.orm import sessionmaker, declarative_base, validates, relationship
from typing_extensions import Self, Type

from lang_pack.lang import LANG_GENERAL

engine = create_engine('sqlite:///data/database.db')
engine.connect()

Session = sessionmaker(bind=engine)
session = Session()


class General:
    """
    Parent class for ORM models
    """

    def save(self) -> Self:
        """
        Save ORM model
        :return: Self
        """

        try:
            session.add(self)
            session.commit()
            session.refresh(self)
            return self
        except Exception as e:
            session.rollback()
            raise Exception(e)

    def delete(self) -> bool | None:
        """
        Delete ORM model
        :return: bool | None
        """
        try:
            session.delete(self)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise Exception(e)

    @classmethod
    def get_one(cls, filter_: dict[str, int | str]) -> Any:
        """
        Get one ORM
        Example for filter_ and order_"
        - filter_: {'field1': 3, 'field2': 'some_value'}
        :param filter_: dict
        :return: TagOrm | ValueOrm
        """
        filter_expression = [func.lower(getattr(cls, k)) == func.lower(v) for k, v in filter_.items()]
        return session.query(cls).filter(and_(*filter_expression)).first()

    @classmethod
    def get_all(cls,
                filter_: dict[str, int | str] = None,
                order_: dict[str, Callable] = None,
                tags: list[int] = None,
                limit: int = None) -> list[Any]:
        """
        Get ORMs
        Example for filter_ и order_:
        - filter_: {'field1': 3, 'field2': 'some_value'}
        - order_: {'field1': asc, 'field2': desc}
        :param filter_: dict = None
        :param order_: dict = None
        :param tags: list[int] = None
        :param limit: int = None
        :return: list[TagOrm | ValueOrm]
        """

        query = session.query(cls)
        if filter_:
            query = query.filter(and_(*filter_))
        if tags:
            query = query.filter(cls.tags.any(TagOrm.id.in_(i for i in tags)))
        if order_:
            order_expression = [fn(getattr(cls, field)) for field, fn in order_.items()]
            query = query.order_by(*order_expression)
        if limit:
            query = query.limit(limit)
        return query.all()


Base = declarative_base(cls=General)

values_tags = Table(
    'values_tags',
    Base.metadata,
    Column('value_id', ForeignKey('values.id')),
    Column('tag_id', ForeignKey('tags.id'))
)


class TagOrm(Base):
    __tablename__ = 'tags'
    id = Column(Integer, name='id', nullable=False, primary_key=True, autoincrement=True)
    name = Column(String(50), name='name', nullable=False, unique=True)

    @validates('name')
    def strip_value(self, key, value):
        if isinstance(value, str):
            return value.strip()
        return value

    def __repr__(self) -> str:
        return "TagOrm({id}, '{name}')".format(id=self.id, name=self.name)


class TypeEnum(enum.Enum):
    VIN = LANG_GENERAL["income"]
    VOUT = LANG_GENERAL["expense"]


class ValueOrm(Base):
    __tablename__ = 'values'
    id = Column(Integer, name='id', nullable=False, primary_key=True, autoincrement=True)
    type = Column(Enum(TypeEnum), index=True, nullable=False)
    message = Column(String(10000), name='message')
    price_usd = Column(Float, name='price_usd')
    price_gel = Column(Float, name='price_gel')
    date = Column(DateTime, name='date')
    tags = relationship('TagOrm', secondary=values_tags, lazy=True)

    @validates('message')
    def strip_value(self, key, value):
        if isinstance(value, str):
            return value.strip()
        return value

    def __repr__(self) -> str:
        return "ValueOrm({id}, {type}, {date})".format(id=self.id, type=self.type, date=self.date)

    @classmethod
    def get_years_range(cls) -> list:
        return session.query(extract('year', getattr(cls, 'date')).label('year')) \
                        .distinct().order_by(desc('year')).all()


def init_db():
    Base.metadata.create_all(engine)

