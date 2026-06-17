import os
import sys

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

PROFILE_FILE = "profile.json"

MENU_IMAGES = {
    # Appetizers
    "سالاد الویه": resource_path(os.path.join("media", "appetizers", "salad-olviye.webp")),
    "سالاد سزار": resource_path(os.path.join("media", "appetizers", "ceaser-salad.webp")),
    "سوپ مرغ": resource_path(os.path.join("media", "appetizers", "chicken-soup.webp")),
    "کشک بادمجان": resource_path(os.path.join("media", "appetizers", "kashk-bademjoon.webp")),
    "سمبوسه": resource_path(os.path.join("media", "appetizers", "sambooseh.webp")),
    # Main dishes
    "قرمه سبزی": resource_path(os.path.join("media", "foods", "ghormeh-sabzi.webp")),
    "جوجه کباب": resource_path(os.path.join("media", "foods", "joojeh kabab.webp")),
    "کباب کوبیده": resource_path(os.path.join("media", "foods", "kabab.webp")),
    "زرشک پلو با مرغ": resource_path(os.path.join("media", "foods", "zereshk-polo.webp")),
    "خورشت قیمه": resource_path(os.path.join("media", "foods", "gheimeh.webp")),
    "استیک": resource_path(os.path.join("media", "foods", "steak.webp")),
    # Beverages
    "دلستر": resource_path(os.path.join("media", "beverages", "delester.webp")),
    "نوشابه": resource_path(os.path.join("media", "beverages", "nooshabeh.webp")),
    "دوغ": resource_path(os.path.join("media", "beverages", "doogh.webp")),
    "آب معدنی": resource_path(os.path.join("media", "beverages", "mineral-water.webp")),
    # Desserts
    "بستنی سنتی": resource_path(os.path.join("media", "desserts", "bastani-sonnati.webp")),
    "شله زرد": resource_path(os.path.join("media", "desserts", "shole-zard.webp")),
    "فرنی": resource_path(os.path.join("media", "desserts", "fereni.webp")),
    "کیک شکلاتی": resource_path(os.path.join("media", "desserts", "Cake.webp")),
    "فالوده شیرازی": resource_path(os.path.join("media", "desserts", "faloodeh.webp")),
}

MENU_DATA = {
    "Pish Ghaza": {
        "سالاد الویه": 150000,
        "سالاد سزار": 300000,
        "سوپ مرغ": 280000,
        "کشک بادمجان": 320000,
        "سمبوسه": 125000,
    },
    "Ghaza Asli": {
        "قرمه سبزی": 350000,
        "جوجه کباب": 350000,
        "کباب کوبیده": 380000,
        "زرشک پلو با مرغ": 370000,
        "خورشت قیمه": 320000,
        "استیک": 850000,
    },
    "Nooshidani": {
        "دلستر": 65000,
        "نوشابه": 70000,
        "دوغ": 65000,
        "آب معدنی": 20000,
    },
    "Deser": {
        "بستنی سنتی": 150000,
        "شله زرد": 200000,
        "فرنی": 180000,
        "کیک شکلاتی": 150000,
        "فالوده شیرازی": 145000,
    },
}
