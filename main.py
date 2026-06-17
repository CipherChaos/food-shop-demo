import sys
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)

    font_id = QFontDatabase.addApplicationFont("media/fonts/Vazirmatn.ttf")
    if font_id != -1:
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
            vazir_family = font_families[0]
            app.setFont(QFont(vazir_family, 10))

    app.setStyle("Fusion")
    from app.restaurant_app import RestaurantOrderApp
    window = RestaurantOrderApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()