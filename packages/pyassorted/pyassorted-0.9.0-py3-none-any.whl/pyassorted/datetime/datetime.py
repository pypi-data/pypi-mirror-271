import datetime
from typing import Text, Union

import pytz


def aware_datetime_now(
    tz: Union[Text, "pytz.BaseTzInfo"] = pytz.UTC
) -> "datetime.datetime":
    """Get the current datetime in the specified timezone.

    Parameters
    ----------
    tz : Union[Text, pytz.BaseTzInfo], optional
        The timezone, by default pytz.UTC

    Returns
    -------
    datetime.datetime
        The current datetime in the specified timezone.
    """

    tz = pytz.timezone(tz) if isinstance(tz, Text) else tz
    utc_dt = pytz.UTC.localize(datetime.datetime.utcnow())
    return utc_dt.astimezone(tz)


def iso_datetime_now(tz: Union[Text, "pytz.BaseTzInfo"] = pytz.UTC) -> Text:
    """Get the current datetime in the specified timezone as an ISO 8601 string.

    Parameters
    ----------
    tz : Union[Text, pytz.BaseTzInfo], optional
        The timezone, by default pytz.UTC

    Returns
    -------
    Text
        The current datetime in the specified timezone as an ISO 8601 string.
    """

    return aware_datetime_now(tz).isoformat()


def to_timezone(
    value: Union[Text, "pytz.BaseTzInfo", "datetime.timezone"]
) -> "datetime.timezone":
    """Convert a timezone value to a datetime.timezone object.

    Parameters
    ----------
    value : Union[Text, pytz.BaseTzInfo, datetime.timezone]
        The timezone value.

    Returns
    -------
    datetime.timezone
        The timezone as a datetime.timezone object.
    """

    if isinstance(value, Text):
        try:
            tzinfo = datetime.datetime.fromisoformat(value).tzinfo

        except ValueError:
            try:
                tzinfo = datetime.timezone(
                    datetime.datetime.now(pytz.timezone(value)).utcoffset()
                )

            except Exception:
                raise ValueError(f"Invalid timezone value: {value}")

    elif isinstance(value, pytz.BaseTzInfo):
        tzinfo = datetime.timezone(datetime.now(value).utcoffset())

    elif isinstance(value, datetime.timezone):
        tzinfo = value
    else:
        raise ValueError(f"Invalid timezone value: {value}")

    return tzinfo
