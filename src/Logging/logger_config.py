import logging
import pytz
from datetime import datetime, timezone
import config


def utc_to_local(*args):
    utc_dt = datetime.now(timezone.utc)
    my_timezone = pytz.timezone(config.TIMEZONE)
    converted = utc_dt.replace(tzinfo=pytz.utc).astimezone(tz=my_timezone)
    return converted.timetuple()


logging.Formatter.converter = utc_to_local
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename=None if config.MODE == "DEV" else "bot.log",
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
