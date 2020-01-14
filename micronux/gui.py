# module: gui.py
#
# Import PySide2, load .ui file
# and show window.
# note: main needs sys module and
# end with sys.exit(app.exec_())

import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QFileDialog
from PySide2.QtCore import QFile, Qt
from PySide2.QtGui import QIcon

### just to remove an ugly error message
from PySide2.QtCore import QCoreApplication
QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

# make_gui(
#   .ui file,
#   window title,
#   style
# )
def make_gui(gui_file, title='Untitled', style='fusion'):
    app = QApplication(sys.argv)
    app.setStyle(style)

    ui_file = QFile(gui_file)
    ui_file.open(QFile.ReadOnly)
    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()

    ### Setup and show window
    window.setWindowTitle(title)
    window.setWindowIcon(QIcon('micronux/icon.png'))
    window.show()

    return {'app': app,'window': window}
