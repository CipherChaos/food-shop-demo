import os
from PyQt5.QtWidgets import QMessageBox
from .date_utils import get_jalali_date_str

try:
    from openpyxl import Workbook
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False

try:
    from openpyxl import Workbook
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False


def export_order_to_excel(cart: list, parent=None) -> bool:
    """
    Create an Excel invoice for the given cart and save it to the 'reports/' folder.
    Returns True if the file was successfully saved, False otherwise.
    """
    if not EXCEL_AVAILABLE:
        QMessageBox.warning(
            parent,
            "هشدار",
            "کتابخانه openpyxl نصب نیست. فایل اکسل ایجاد نشد.\n"
            "برای نصب: pip install openpyxl"
        )
        return False

    try:
        wb = Workbook()
        ws = wb.active
        ws.title = "فاکتور"
        ws.sheet_view.rightToLeft = True

        # Headers
        headers = ["نام غذا", "قیمت واحد (تومان)", "تعداد", "جمع (تومان)"]
        ws.append(headers)

        # Cart items
        for item in cart:
            name = item["name"]
            price = item["price"]
            qty = item["qty"]
            ws.append([name, price, qty, price * qty])

        total = sum(item["price"] * item["qty"] for item in cart)
        ws.append(["جمع کل", "", "", total])

        # Generate filename with current date
        date_str = get_jalali_date_str()
        filename = f"فاکتورفروش_{date_str}.xlsx"

        # Ensure reports directory exists
        reports_dir = os.path.join(os.getcwd(), "reports")
        os.makedirs(reports_dir, exist_ok=True)

        filepath = os.path.join(reports_dir, filename)
        wb.save(filepath)

        QMessageBox.information(
            parent,
            "موفق",
            f"فاکتور با موفقیت ذخیره شد:\n{filepath}"
        )
        return True

    except Exception as e:
        QMessageBox.critical(
            parent,
            "خطا",
            f"خطا در ایجاد فایل اکسل:\n{str(e)}"
        )
        return False
