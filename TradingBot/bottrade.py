import datetime
from botlog import BotLog
import colorama
import crayons
colorama.init()


class BotTrade(object):
    def __init__(self, currentPrice, stopLossEdge):
        self.output = BotLog()
        self.status = "OPEN"
        self.entryPrice = currentPrice
        self.exitPrice = 0
        self.pnl= 0
        self.side= "Buy"
        self.entryTime= datetime.datetime.now()
        self.exitTime = ""
        self.output.log("Trade opened")
        self.stopLoss = currentPrice-stopLossEdge

    def close(self, currentPrice):
        self.exitTime = datetime.datetime.now()
        self.status = "CLOSED"
        self.side = "Sell"
        self.exitPrice = currentPrice
        self.output.log("Trade closed")
        self.pnl = self.exitPrice - self.entryPrice

        tradeStatus = "Entry Price: " + str(round(self.entryPrice, 3)) + " Status: " + \
                      str(self.status) + " Exit Price: " + str(round(self.exitPrice, 3))
        tradeStatus = tradeStatus + " Pnl: " + str(round(self.pnl, 3))
        if (self.pnl>0):
            tradeStatus = crayons.green(tradeStatus)
        else:
            tradeStatus = crayons.red(tradeStatus)
        self.output.log(tradeStatus)


    def tick(self, currentPrice):
        if (self.stopLoss>0):
            if (currentPrice <= self.stopLoss):
                self.output.log(crayons.magenta("Exit By Stop Loss"))
                self.close(currentPrice)

    def showStatus(self):
        if (self.status == "OPEN"):
            tradeStatus = "Entry Price: " + str(round(self.entryPrice, 3)) + " Status: " + str(self.status)
            tradeStatus= crayons.yellow(tradeStatus)
            self.output.log(tradeStatus)

