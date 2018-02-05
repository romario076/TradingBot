
class tradesData(object):

   def __init__(self):
       self.tradesData= []

   def addTrades(self, entryTime, exitTime, pair, entryPrice, exitPrice, side, pnl):
       self.tradesData.append([str(entryTime), str(exitTime), pair, entryPrice, exitPrice, side, pnl])
