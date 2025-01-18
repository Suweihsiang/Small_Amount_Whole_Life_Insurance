import sys
from myMainWindow import QmyMainWindow
from PyQt5.QtWidgets import QApplication


if __name__=="__main__":
    app=QApplication(sys.argv)
    form=QmyMainWindow()
    form.showMaximized()
    sys.exit(app.exec_())