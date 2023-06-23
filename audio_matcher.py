import sys

from PySide6.QtWidgets import QApplication
from qt_material import build_stylesheet

from view.main import MainWindow


if __name__ == '__main__':
    # init
    app = QApplication([])
    main_window = MainWindow()

    # style setting
    stylesheet = build_stylesheet(theme="dark_teal.xml", template="material.css")
    main_window.stylesheet = stylesheet
    app.setStyleSheet(stylesheet)

    # start app
    main_window.show()
    app_thread = app.exec()

    # end
    sys.exit(app_thread)
