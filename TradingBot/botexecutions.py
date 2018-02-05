
class executionsData(object):

   def __init__(self):
       self.execData= []

   def addExecutions(self, entryTime, pair, entryPrice, side, pnl):
       self.execData.append([str(entryTime), pair, entryPrice, side, pnl])

