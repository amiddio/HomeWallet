from typing_extensions import Self, Type

from models.scheme import TagOrm, ValueOrm


class BaseModel:

    def get(self) -> Type[TagOrm | ValueOrm]:
        return self.orm

    def set(self, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self.orm, k, v)

    def save(self) -> Self:
        self.orm.save()
        return self

    def delete(self) -> bool:
        return self.orm.delete()
