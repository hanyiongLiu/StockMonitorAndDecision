from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sys


class Strategy(QWidget):
    def __init__(self):
        super(Strategy, self).__init__()

        self.product_name = None
        self.buy_reason = None
        self.current_price = None
        self.buying_price = None
        self.stop_profit_price = None
        self.stop_loss_price = None
        self.ratio = None
        self.buying_point = None
        self.selling_point = 'yes'

        self.initUI()

    def initUI(self):
        self.product_details()
        self.setWindowTitle('Strategy')
        self.resize(300, 100)

    def product_details(self):
        ###product
        self.edit_name = QLineEdit()
        self.edit_name.setAlignment(Qt.AlignRight)
        # self.edit_name.textChanged.connect(self.text_change)

        ####buy reason
        self.reason_combo = QComboBox()
        self.reason_combo.addItem('无')
        self.reason_combo.addItem('回调')
        self.reason_combo.addItem('多次极值点')
        self.reason_combo.currentIndexChanged.connect(self.get_reason)

        ###current price
        self.current_price_label = QLabel()
        self.current_price_label.setText(self.current_price)

        ###buying price
        self.edit_buying_price = QLineEdit()
        self.edit_buying_price.setAlignment(Qt.AlignRight)

        ###stop profit price
        self.edit_stop_profit_price = QLineEdit()
        self.edit_stop_profit_price.setAlignment(Qt.AlignRight)

        ###stop loss price
        self.edit_stop_loss_price = QLineEdit()
        self.edit_stop_loss_price.setAlignment(Qt.AlignRight)

        ###the ratio of profit and loss
        self.label_ratio = QLabel()
        self.label_ratio.setText(self.ratio)

        ###whether reach the buying price
        self.label_buying_point = QLabel()
        self.label_buying_point.setText(self.buying_point)

        ###whether reach the selling price
        self.label_selling_point = QLabel()
        self.label_selling_point.setText(self.selling_point)

        ###decision buttion
        self.button_decision = QPushButton('决策')
        self.button_decision.clicked.connect(self.onClick_make_decision)

        form_layout = QFormLayout()
        form_layout.addRow('产品：', self.edit_name)
        form_layout.addRow('买入理由:', self.reason_combo)
        form_layout.addRow('当前价格:', self.current_price)
        form_layout.addRow('买入价格:', self.edit_buying_price)
        form_layout.addRow('止盈价格:', self.edit_stop_profit_price)
        form_layout.addRow('止损价格:', self.edit_stop_loss_price)
        form_layout.addRow('盈亏比:', self.label_ratio)
        form_layout.addRow('到达买入点:', self.label_buying_point)
        form_layout.addRow('到达卖出点:', self.label_selling_point)
        form_layout.addRow(self.button_decision)

        self.setLayout(form_layout)

    def text_change(self):
        if self.sender() == self.edit_name:
            product_name = self.edit_name.text()
            print(product_name)

    def get_reason(self, i):
        self.buy_reason = self.reason_combo.currentText()
        print(self.buy_reason)

    def onClick_make_decision(self):
        if not self.edit_name.text() or not self.edit_buying_price.text() \
                or not self.edit_stop_profit_price.text() or not self.edit_stop_loss_price.text():
            self.button_decision.setToolTip('请输入完整信息')
        else:
            self.product_name = self.edit_name.text()
            self.buy_reason = self.reason_combo.currentText()
            # TODO: self.current_price
            self.buying_price = self.edit_buying_price.text()
            self.stop_profit_price = self.edit_stop_profit_price.text()
            self.stop_loss_price = self.edit_stop_loss_price.text()
            self.ratio = round(abs((float(self.stop_profit_price) - float(self.buying_price)) / (
                    float(self.stop_loss_price) - float(self.buying_price))), 2)
            # TODO:
            # self.buying_point
            # self.selling_point

            if self.buy_reason == '无':
                self.label_ratio.setText('<font color = red>不购买</font>')
            else:
                self.label_ratio.setText('<font color = green>{}</font>'.format(str(self.ratio)))


def main():
    app = QApplication(sys.argv)
    main = Strategy()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
