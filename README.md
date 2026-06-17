# Food Shop Demo

A demo food shop application developed with PyQT for POC (proof of concept) and learning purposes. 

## About

This is a simple food shop demo built with PyQT to showcase basic GUI application development with Python. The project Saas point for understanding how to structure a PyQT application.

## Project Structure

```
food-shop-demo/
├── app/                    # Application modules
├── docs/                   # Documentation
├── media/                  # Images and assets
├── reports/                # Generated reports
├── tests/                  # Unit tests
├── main.py                 # Application entry point
├── profile.json            # User profile configuration
└── requirements.txt        # Python dependencies
```

## Installation

To get started with the project, clone this repository:

```bash
git clone https://github.com/CipherChaos/food-shop-demo.git
```

Make sure you are in the project directory:

```bash
cd food-shop-demo
```

Create and activate a virtual environment (recommended):

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv venv
source .venv/bin/activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the project:

```bash
python main.py
```

## Building Executables

Build standalone executables using PyInstaller.

### Windows

Create FoodShopDemo.exe:

```bash
pyinstaller --name FoodShopDemo --onefile --windowed --add-data "app;app" --add-data "media;media" main.py
```

Inside the `dist/` directory you can find `FoodShopDemo.exe`

### Linux

Create Linux binary:

```bash
pyinstaller --name FoodShopDemo --onefile --windowed --add-data "app:app" --add-data "media:media" main.py
```

Make executable:

```bash
chmod +x dist/FoodShopDemo
```

**Add to Linux Applications Menu (Optional):**

1. Create and open the desktop file:
```bash
nano ~/.local/share/applications/foodshopdemo.desktop
```

2. Add the following configuration (adjust paths as needed):
```ini
[Desktop Entry]
Type=Application
Name=Food Shop Demo
Exec=/home/YOURUSER/path/to/FoodShopDemo
Icon=/home/YOURUSER/path/to/media/icon.png
Terminal=false
Categories=Utility;
```

3. Make desktop file executable:
```bash
chmod +x ~/.local/share/applications/foodshopdemo.desktop
```

4. Copy binary to system path (optional):
```bash
sudo cp dist/FoodShopDemo /usr/local/bin/
```

## Status

This is a demo project - feel free to explore, learn from it, and build upon it.

## License

MIT License

## Author

Ariyan Bolandi ([CipherChaos](https://github.com/CipherChaos))
