from PyQt5 import QtCore
from qgis.utils import iface
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon

class QgisCtrl:

    def addActionDigitizeToolBar(self, action):
        iface.digitizeToolBar().addAction(action)

    def removeActionDigitizeToolBar(self, action):
        iface.digitizeToolBar().removeAction(action)

    def createAction(self, name, iconPath, callback):
        a = QAction(
            QIcon(iconPath),
            name,
            iface.mainWindow()
        )
        a.triggered.connect(callback)
        return a

    def addDockWidget(self, dockWidget):
        iface.addDockWidget(QtCore.Qt.RightDockWidgetArea, dockWidget)
    
    def removeDockWidget(self, dockWidget):
        if not dockWidget.isVisible():
            return
        iface.removeDockWidget(dockWidget)
