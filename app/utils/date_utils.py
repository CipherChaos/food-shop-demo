from datetime import datetime

try:
    import jdatetime
    JALALI_AVAILABLE = True
except ImportError:
    JALALI_AVAILABLE = False


def get_jalali_date_str() -> str:
    """
    Return the current date as a string in YYYYMMDD format.
    Uses Jalali (Persian) calendar if the jdatetime library is installed,
    otherwise falls back to Gregorian.
    """
    if JALALI_AVAILABLE:
        today = jdatetime.date.today()
        return f"{today.year:04d}{today.month:02d}{today.day:02d}"
    else:
        return datetime.now().strftime("%Y%m%d")
