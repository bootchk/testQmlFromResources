'''
Demonstrate problem loading qml resources when pyqtdeployed.

App whose outer QWidget has icon and widget with embedded QML, both loaded from resources.
Loading icon works, but loading qml fails.
'''
import sys

from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QToolButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl, QFileInfo
from PyQt5.QtQuick import QQuickView


class WidgetApp(object):
  
  def __init__(self):
    
    app = QApplication(sys.argv)
    
    mainWindow = QWidget()
    mainWindow.setGeometry(100, 100, 500, 400)
    mainWindow.show()
    
    layout = QVBoxLayout()
    layout.addWidget(self.widgetEmbeddingQmlFromResources(parentWindow=mainWindow))
    layout.addWidget(self.iconButtonFromResources())
    
    mainWindow.setLayout(layout)
    
    sys.exit(app.exec_())
    

  def widgetEmbeddingQmlFromResources(self, parentWindow):
    " Widget containing QuickView of qml loaded from resources "
    
    quickView = QQuickView()
    
    # quickView.setSource requires a QUrl
    '''
    ??? Why does this require '/appPackage' prefix, unlike for icon resource?
    This works when invoked from Python.
    But when pyqtdeployed, it fails, the app prints:
    
    file:///home/bootch/pensoolpyqtdeploy/:/appPackage/qml/toolBar.qml: File not found
    resourceRoot:  :/
    qml QUrl:  file::/appPackage/qml/toolBar.qml
    '''
    rootedQmlFilename = self.resourceRoot() + '/appPackage/qml/toolBar.qml'
    '''
    I also tried:
    rootedQmlFilename = self.resourceRoot() + '/qml/toolBar.qml'
    Which fails invoked from Python, AND when pyqtdeployed.
    '''
    
    qmlUrl=QUrl.fromLocalFile(rootedQmlFilename)
    # I also tried: qmlUrl=QUrl(rootedQmlFilename)
    # I also tried: qmlUrl=QUrl("qrc:/qml/toolBar.qml")
    # I also tried: qmlUrl=QUrl("qrc:/appPackage/qml/toolBar.qml")
    assert qmlUrl.isValid()
    assert not qmlUrl.isEmpty()
    assert not qmlUrl.toString() == ''
    #assert qmlUrl.isLocalFile()
    print("qml QUrl: ", qmlUrl.toString())
    quickView.setSource(qmlUrl)
    
    # embed in widget
    widget = QWidget.createWindowContainer(quickView, parent=parentWindow)
    
    return widget
    

  def iconButtonFromResources(self):
    button = QToolButton()
    icon = QIcon(self.resourceRoot() + '/images/pensool.png')
    button.setIcon(icon)
    return button
  
  
  def resourceRoot(self):
    result = QFileInfo(__file__).absolutePath()
    print("resourceRoot: ", result)
    return result


app = WidgetApp()

  
  
  