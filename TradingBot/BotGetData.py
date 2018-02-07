
import pandas as pd
from poloniex import Poloniex
import time
import datetime



class BotGetData(object):

    def __init__(self, pair, peroid):
        self.pair= pair
        self.period= peroid
        self.conn = Poloniex("YourID", "YourKey")
        BotGetData.getHistoricalData(self)
        self.lastPrice= 0
        self.percentChange= 0
        self.askPrice= 0
        self.bidPrice= 0

    def getHistoricalData(self):
        startTime = str(datetime.datetime.now() - datetime.timedelta(hours=1))[:19]
        startTimeUnix = time.mktime(datetime.datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S").timetuple())

        endTime = str(datetime.datetime.now())[:19]
        endTimeUnix = time.mktime(datetime.datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S").timetuple())

        dd = self.conn.returnChartData(currencyPair=self.pair, start=startTimeUnix, end=endTimeUnix, period=300)
        dd = pd.DataFrame(dd)
        dd.date = [pd.Timestamp(datetime.datetime.fromtimestamp(x).strftime("%Y-%m-%d %H:%M:%S")) for x in dd.date]
        dd.weightedAverage = dd.weightedAverage.astype(float)
        prices = dd[["date", "weightedAverage"]]
        prices.columns= ["Date", "Price"]
        prices["Ask"]= prices.Price
        prices["Bid"] = prices.Price
        self.historicalData= prices

    def getLastPrice(self):
        self.lastPrice = float(self.conn.returnTicker()[self.pair]["last"])

    def getBestBid(self):
        self.bidPrice = float(self.conn.returnTicker()[self.pair]["highestBid"])

    def getBestAsk(self):
        self.askPrice = float(self.conn.returnTicker()[self.pair]["lowestAsk"])

    def getPercentChange(self):
        self.percentChange = float(self.conn.returnTicker()[self.pair]["percentChange"])

    def updateData(self):
        self.getLastPrice()
        self.getBestAsk()
        self.getBestBid()
        self.getPercentChange()
        self.historicalData= self.historicalData.append({"Date":datetime.datetime.now(),\
                                            "Price":self.lastPrice, \
                                            "Ask":self.askPrice, \
                                            "Bid": self.bidPrice}, ignore_index=True)

