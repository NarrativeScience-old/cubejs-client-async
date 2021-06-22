"""Contains enums"""

import enum


@enum.unique
class TimeGranularity(enum.Enum):
    """Time granularity"""

    second = "second"
    minute = "minute"
    hour = "hour"
    day = "day"
    week = "week"
    month = "month"
    year = "year"
    null = None


@enum.unique
class Order(enum.Enum):
    """Result ordering directions"""

    asc = "asc"
    desc = "desc"


@enum.unique
class FilterOperator(enum.Enum):
    """Operators used in filters"""

    equals = "equals"
    not_equals = "notEquals"
    contains = "contains"
    not_contains = "notContains"
    gt = "gt"
    gte = "gte"
    lt = "lt"
    lte = "lte"
    is_set = "set"
    not_set = "notSet"
    in_date_range = "inDateRange"
    not_in_date_range = "notInDateRange"
    before_date = "beforeDate"
    after_date = "afterDate"
