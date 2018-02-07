from botlog import BotLog
from bottrade import BotTrade
from botexecutions import executionsData
from bottrades import tradesData
from botMetrics import botMetrics
import pandas as pd
import datetime
import colorama
import crayons
colorama.init()


class BotStrategy(object):

    def __init__(self, prices, pair, lengthMA, openPosLimit, stopLossEdge, entryEdge, timePosEdge):
        self.output = BotLog()
        self.prices = prices
        self.closes = []  # Needed for Momentum Indicator
        self.trades = []
        self.currentPrice = 0
        self.numSimulTrades = openPosLimit
        self.pair= pair
        self.side= ""
        self.lengthMA= lengthMA
        self.movAverage= 0
        self.expMovAverage= 0
        self.strategyTradingMetric= 0
        self.allExecutions = executionsData()
        self.allTrades = tradesData()
        self.metrics= botMetrics()
        self.openedPositions =[]
        self.lastTradePnl=0
        self.totalPnl=0
        self.stopLossEdge= stopLossEdge
        self.entryEdge= entryEdge
        self.timePosEdge= timePosEdge

    def movingAverage(self, data, period):
        ma= 0
        if len(data)> 1:
            ma= sum(data[-period:])/len(data[-period:])
        return(ma)

    def tick(self, price, startTrade):
        self.currentPrice= price
        self.prices.append(self.currentPrice)
        self.movAverage= self.metrics.movingAverage(data=self.prices, period=self.lengthMA)
        self.expMovAverage = self.metrics.EMA(prices=self.prices, period=self.lengthMA)
        self.strategyTradingMetric= self.expMovAverage
        self.output.log("Price: " + str(round(price, 3)) + "  MA: " + str(round(self.movAverage ,3)) + \
                 "  EMA: "+str(round(self.expMovAverage ,3)))

        if startTrade:
            self.evaluatePositions()
            if self.stopLossEdge>0:
                self.updateOpenTrades()
            self.showPositions()
            self.updateOpenPositions()

    def evaluatePositions(self):
        currentTime= datetime.datetime.now()
        openTrades = []
        for trade in self.trades:
            if (trade.status == "OPEN"):
                openTrades.append(trade)

        if (len(openTrades) < self.numSimulTrades):
            if ((self.strategyTradingMetric-self.currentPrice)> self.entryEdge):
                btrade= BotTrade(self.currentPrice, stopLossEdge=self.stopLossEdge)
                self.trades.append(btrade)
                self.updateExecutions(trade=btrade, executionTime=btrade.entryTime, executionPrice=btrade.entryPrice)

        for trade in openTrades:
            if (self.currentPrice > self.strategyTradingMetric):
                if (currentTime-trade.entryTime).seconds>self.timePosEdge:
                    trade.close(self.currentPrice)
                    self.updateExecutions(trade=trade, executionTime=trade.exitTime, executionPrice=trade.exitPrice)
                    self.updateTrades(trade=trade)
                    self.lastTradePnl= trade.pnl
                    self.totalPnl= self.totalPnl+self.lastTradePnl

    def closeAll(self):
        for trade in self.trades:
            if (trade.status == "OPEN"):
                trade.close(self.currentPrice)
                self.updateExecutions(trade=trade, executionTime=trade.exitTime, executionPrice=trade.exitPrice)
                self.updateTrades(trade=trade)
                self.lastTradePnl = trade.pnl
                self.totalPnl = self.totalPnl + self.lastTradePnl
        self.trades= []
        self.openedPositions =[]


    def updateExecutions(self, trade, executionTime, executionPrice):
        self.allExecutions.addExecutions(entryTime=executionTime, pair=self.pair, \
                                         entryPrice=executionPrice, side=trade.side, pnl=trade.pnl)
    def updateTrades(self, trade):
        self.allTrades.addTrades(entryTime=trade.entryTime, exitTime=trade.exitTime, pair=self.pair,\
                                 entryPrice=trade.entryPrice, exitPrice=trade.exitPrice, side=trade.side,
                                 pnl=trade.pnl)
    def updateOpenTrades(self):
        for trade in self.trades:
            if (trade.status == "OPEN"):
                if (self.currentPrice < trade.stopLoss):
                    print("Exit StopLoss")
                    self.output.log(crayons.magenta("Exit By Stop Loss"))
                    trade.close(self.currentPrice)
                    self.updateExecutions(trade=trade, executionTime=trade.exitTime, executionPrice=trade.exitPrice)
                    self.updateTrades(trade=trade)
                    self.lastTradePnl = trade.pnl
                    self.totalPnl = self.totalPnl + self.lastTradePnl

    def updateOpenPositions(self):
        openedPositions = []
        for trade in self.trades:
            if (trade.status=="OPEN"):
                openedPositions.append([trade.entryTime, self.pair, trade.side, \
                                       round(trade.entryPrice,2), round(trade.pnl,2)])
        self.openedPositions= openedPositions


    def showPositions(self):
        openedPositions= []
        for trade in self.trades:
            trade.showStatus()
        return openedPositions

    def showOpenedPositions(self):
        temp= pd.DataFrame(self.openedPositions)
        if len(temp)>0:
            temp.columns= ["Time", "Pair", "Side", "EntryPrice", "Pnl"]
        return temp

    def showExecutions(self):
        temp= pd.DataFrame(self.allExecutions.execData)
        if len(temp)>0:
            temp.columns= ["Time", "Pair", "Price", "Side", "Pnl"]
        return temp

    def showTrades(self):
        temp = pd.DataFrame(self.allTrades.tradesData)
        if len(temp) > 0:
            temp.columns = ["EntryTime", "ExitTime", "Pair", "EntryPrice", "ExitPrice", "Side", "Pnl"]
        return temp

    def clearExecutions(self):
        self.allExecutions = executionsData()
        self.allTrades = tradesData()
