import sys
from PyQt6.QtWidgets import QApplication
from gui import ModernUI
from autoclicker import AutoclickerController
from hardware import WindowsInputHandler

def main():
    app = QApplication(sys.argv)

    hw_handler = WindowsInputHandler()
    controller = AutoclickerController(hw_handler)
    controller.start()

    window = ModernUI(controller)
    window.show()

    exit_code = app.exec()

    controller.stop()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
