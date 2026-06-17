import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

import pytest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from app.core.cart_manager import CartManager


@pytest.fixture(scope="session")
def qapp():
    """Create a single QApplication for the whole test session."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app
    # We do not quit here – the cleanup fixture handles it


@pytest.fixture(scope="session", autouse=True)
def cleanup_qt(qapp):
    """Force deletion of all Qt objects before session ends to avoid segfault."""
    yield
    app = QApplication.instance()
    if app:
        # Delete all top‑level widgets
        for widget in app.topLevelWidgets():
            widget.deleteLater()
        # Process all pending deletion events
        app.processEvents()
        # Now it is safe to quit
        app.quit()


@pytest.fixture
def cart():
    """Return a fresh, empty CartManager for each test."""
    return CartManager()