import os

PROFILE_FILE = "profile.json"

MENU_IMAGES = {
    # Appetizers
    "سالاد الویه": os.path.join("media", "appetizers", "salad-olviye.webp"),
    "سالاد سزار": os.path.join("media", "appetizers", "ceaser-salad.webp"),
    "سوپ مرغ": os.path.join("media", "appetizers", "chicken-soup.webp"),
    "کشک بادمجان": os.path.join("media", "appetizers", "kashk-bademjoon.webp"),
    "سمبوسه": os.path.join("media", "appetizers", "sambooseh.webp"),
    # Main dishes
    "قرمه سبزی": os.path.join("media", "foods", "ghormeh-sabzi.webp"),
    "جوجه کباب": os.path.join("media", "foods", "joojeh kabab.webp"),
    "کباب کوبیده": os.path.join("media", "foods", "kabab.webp"),
    "زرشک پلو با مرغ": os.path.join("media", "foods", "zereshk-polo.webp"),
    "خورشت قیمه": os.path.join("media", "foods", "gheimeh.webp"),
    "استیک": os.path.join("media", "foods", "steak.webp"),
    # Beverages
    "دلستر": os.path.join("media", "beverages", "delester.webp"),
    "نوشابه": os.path.join("media", "beverages", "nooshabeh.webp"),
    "دوغ": os.path.join("media", "beverages", "doogh.webp"),
    "آب معدنی": os.path.join("media", "beverages", "mineral-water.webp"),
    # Desserts
    "بستنی سنتی": os.path.join("media", "desserts", "bastani-sonnati.webp"),
    "شله زرد": os.path.join("media", "desserts", "shole-zard.webp"),
    "فرنی": os.path.join("media", "desserts", "fereni.webp"),
    "کیک شکلاتی": os.path.join("media", "desserts", "Cake.webp"),
    "فالوده شیرازی": os.path.join("media", "desserts", "faloodeh.webp"),
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
