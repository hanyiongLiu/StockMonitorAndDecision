import sys
import strategy
from PyQt5.QtWidgets import QApplication, QDialog






def main():
    myapp=QApplication(sys.argv)
    myDlg=QDialog()
    myUI=strategy.Ui_Dialog(myDlg)
    # myUI.setupUi(myDlg)
    myDlg.show()
    sys.exit(myapp.exec_())


if __name__ == '__main__':
    main()
