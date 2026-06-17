import os
import pytest
from unittest.mock import patch
from app.utils.excel_export import export_order_to_excel

class TestExcelExport:
    @pytest.fixture
    def cart(self):
        return [
            {"name": "آب", "price": 10000, "qty": 2},
            {"name": "نان", "price": 5000, "qty": 1}
        ]

    def test_export_creates_file(self, tmp_path, cart):
        with patch("os.getcwd", return_value=str(tmp_path)):
            success = export_order_to_excel(cart)
            assert success
            report_dir = tmp_path / "reports"
            assert report_dir.exists()
            files = list(report_dir.glob("فاکتورفروش_*.xlsx"))
            assert len(files) == 1

    def test_export_when_openpyxl_missing(self, cart):
        with patch("app.utils.excel_export.EXCEL_AVAILABLE", False):
            with patch("app.utils.excel_export.QMessageBox.warning") as mock_warn:
                result = export_order_to_excel(cart)
                mock_warn.assert_called_once()
                assert result is False