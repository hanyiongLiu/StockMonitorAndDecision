from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QTimer
import sys

import requests
import json


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
        self.margin = None
        self.buying_flag = False
        self.selling_flag = False

        self.timer = QTimer()

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

        ###the margin
        self.label_margin = QLabel()
        self.label_margin.setText(self.margin)

        ###whether reach the buying price
        self.label_buying_flag = QLabel()
        self.label_buying_flag.setText(None)

        ###whether reach the selling price
        self.label_selling_flag = QLabel()
        self.label_selling_flag.setText(None)

        ###judgment buttion
        self.button_decision = QPushButton('判定')
        self.button_decision.clicked.connect(self.onClick_make_decision)

        ###perform button
        self.button_perform = QPushButton('执行')
        self.button_perform.clicked.connect(self.onClick_perform)

        form_layout = QFormLayout()
        form_layout.addRow('产品：', self.edit_name)
        form_layout.addRow('买入理由:', self.reason_combo)
        form_layout.addRow('当前价格:', self.current_price_label)
        form_layout.addRow('买入价格:', self.edit_buying_price)
        form_layout.addRow('止盈价格:', self.edit_stop_profit_price)
        form_layout.addRow('止损价格:', self.edit_stop_loss_price)
        form_layout.addRow('盈亏比:', self.label_ratio)
        form_layout.addRow('涨跌幅：', self.label_margin)
        form_layout.addRow('到达买入点:', self.label_buying_flag)
        form_layout.addRow('到达卖出点:', self.label_selling_flag)
        form_layout.addRow(self.button_decision, self.button_perform)

        self.setLayout(form_layout)

    # def text_change(self):
    #     if self.sender() == self.edit_name:
    #         product_name = self.edit_name.text()
    #         print(product_name)

    def get_reason(self, i):
        self.buy_reason = self.reason_combo.currentText()
        # print(self.buy_reason)

    def onClick_make_decision(self):
        if self.timer.isActive():
            self.timer.stop()
            self.button_perform.setEnabled(True)

        if not self.edit_name.text() or not self.edit_buying_price.text() \
                or not self.edit_stop_profit_price.text() or not self.edit_stop_loss_price.text():
            self.button_decision.setToolTip('请输入完整信息')
        else:
            self.obtain_input()
            self.ratio_judgment()
            self.margin_judgment()

    def obtain_input(self):
        self.product_name = self.edit_name.text()
        self.buy_reason = self.reason_combo.currentText()
        self.buying_price = float(self.edit_buying_price.text())
        self.stop_profit_price = float(self.edit_stop_profit_price.text())
        self.stop_loss_price = float(self.edit_stop_loss_price.text())
        self.ratio = round(abs((self.stop_profit_price - self.buying_price) / (
                self.stop_loss_price - self.buying_price)), 2)

    def ratio_judgment(self):
        if self.buy_reason == '无':
            self.label_ratio.setText('<font color = red size = 5>不购买</font>')
        else:
            self.label_ratio.setText('<font color = green size = 5>{}</font>'.format(str(self.ratio)))

    def margin_judgment(self):
        profit_margin = round(abs(self.stop_profit_price - self.buying_price) / self.buying_price, 4)
        loss_margin = round(abs(self.stop_loss_price - self.buying_price) / self.buying_price, 4)
        self.label_margin.setText(
            '<font color = green size = 5>止盈盈利:{:.2%},止损损失:{:.2%}</font>'.format(profit_margin, loss_margin))

    def obtain_current_price(self):
        stock_name = self.edit_name.text()
        url_name = self.obtain_stock_url(stock_name)

        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.monitor(url_name))
        self.timer.start(10000)

    def onClick_perform(self):
        self.button_perform.setEnabled(False)
        self.label_selling_flag.clear()
        self.label_buying_flag.clear()

        self.obtain_current_price()

    def monitor(self, url_name):

        self.current_price = float(self.spider(url_name))
        self.current_price_label.setText('<font color = red size = 5 >{}</font>'.format(str(self.current_price)))
        # self.current_price_label.repaint()

        self.deal()

    def obtain_stock_url(self, stock_name):
        # stock_name = self.edit_name.text()
        stock_number = {'ETH-USDT': '1640089666667', 'AVAX-USDT': '1640089080391'}
        url_name = 'https://www.okex.com/priapi/v5/market//mult-tickers?t=' + stock_number[
            stock_name] + '&instIds=' + stock_name
        print(url_name)
        return url_name

    def spider(self, url_name):
        session = requests.session()
        response = session.get(url_name, headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'})
        current_price = json.loads(response.text)['data'][0]['last']
        print(current_price)
        return current_price

    def deal(self):
        if self.current_price:
            if abs(self.buying_price - self.current_price) < 0.003 * self.buying_price and not self.buying_flag:
                self.buying_flag = True
                self.label_buying_flag.setText('<font color = red size = 5>买入，价格为{}</font>'.format(self.current_price))
            if self.buying_flag and not self.selling_flag:
                if abs(self.stop_profit_price - self.current_price) < 0.003 * self.buying_price:
                    self.selling_flag = True
                    self.label_selling_flag.setText(
                        '<font color = red size = 5>卖出，止盈价为{}</font>'.format(str(self.current_price)))
                elif abs(self.stop_loss_price - self.current_price) < 0.003 * self.buying_price:
                    self.selling_flag = True
                    self.label_selling_flag.setText(
                        '<font color = red size = 5>卖出，止损价为{}</font>'.format(str(self.current_price)))


def main():
    app = QApplication(sys.argv)
    main = Strategy()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
