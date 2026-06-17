import pytest
from unittest.mock import patch
from app.utils.date_utils import get_jalali_date_str

class TestDateUtils:
    def test_gregorian_fallback(self):
        with patch("app.utils.date_utils.JALALI_AVAILABLE", False):
            date_str = get_jalali_date_str()
            assert len(date_str) == 8
            assert date_str.isdigit()

    def test_jalali_date(self):
        try:
            import jdatetime
            date_str = get_jalali_date_str()
            assert len(date_str) == 8
        except ImportError:
            pytest.skip("jdatetime not installed")