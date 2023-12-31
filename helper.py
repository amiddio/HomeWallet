import calendar
import csv
import datetime as dt

from datetime import datetime
from logger.logger import log
from models.scheme import TypeEnum, ValueOrm
from models.tag_model import TagModel
from models.value_model import ValueModel


def get_year_month_day(date_string: str) -> tuple[int, int, int]:
    """
    Get year, month, day from string date.
    If attribute is empty returned current year, month, day
    :param date_string: str
    :return: tuple[int, int, int]
    """
    if date_string and isinstance(date_string, str):
        result = datetime.strptime(date_string, '%Y-%m-%d')
        return result.year, result.month, result.day
    else:
        return datetime.today().year, datetime.today().month, datetime.today().day


def date_formated(dt):
    return dt.strftime('%d %B, %Y')


def get_last_month():
    previous_year = datetime.now().year
    previous_month = datetime.now().month - 1
    if previous_month == 0:
        previous_month = 12
        previous_year -= 1

    return previous_year, previous_month


def display_price(price, type_=None):
    if not price:
        return ''
    price = "{:,.2f}".format(price)
    if type_ == TypeEnum.VOUT:
        return f"-{price}"
    return price


def prepare_filter_dates(from_date: tuple, to_date: tuple) -> tuple:
    def fn(x):
        return int(x) if x is not None else 0

    from_y, from_m = map(fn, from_date)
    to_y, to_m = map(fn, to_date)
    if not from_m:
        from_m = 12
    if not to_m:
        to_m = 1

    num_days = calendar.monthrange(from_y, from_m)[1]
    start_date = dt.datetime(from_y, from_m, num_days, 23, 59, 59)
    end_date = dt.datetime(to_y, to_m, 1, 00, 00, 00)

    return start_date, end_date


def get_month_number(month: str) -> int | None:
    if not month:
        return

    try:
        datetime_object = dt.datetime.strptime(month, "%B")
        return datetime_object.month
    except ValueError as e:
        log().error(f"ValueError: {str(e)}")


def _get_tag(_tag: str) -> TagModel:
    _tag = _tag.lower().strip()
    tag = TagModel.is_exist(_tag)
    if not tag:
        tag = TagModel(name=_tag).save()
    return tag.get()


def import_data(file_name, type_):
    with open(file_name, 'r', encoding='utf-8') as file:
        rows = csv.reader(file, delimiter=';')
        for i, row in enumerate(rows):
            if i == 0:
                continue
            *_, _msg, _date, _tag, _usd, _gel = row
            result = ValueModel(
                type=type_,
                price_gel=float(_gel) if _gel else None,
                price_usd=float(_usd) if _usd else None,
                date=datetime.strptime(_date, '%Y-%m-%d'),
                message=_msg.strip()
            ).save().add_tags([_get_tag(_tag=_tag)])
            if result:
                print(_msg, _date, _tag, _usd, _gel)
            else:
                raise Exception("Error happened for: ", (_msg, _date, _tag, _usd, _gel))
