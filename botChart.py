
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import pandas as pd
from matplotlib.ticker import  MaxNLocator
import matplotlib.dates as mdates


class botChart(object):
    def __init__(self):
        style.use("dark_background")
        #plt.ion()
        plt.ioff()
        self.fig = plt.figure(figsize=(7, 5))
        self.ax = plt.subplot(111)
        plt.ion()


    def botLiveChart(self, x, y, tradesLive, lastTradePnl, totalPnl, percentChange):

        plt.cla()
        #plt.clf()
        tradesLiveInterval= [j for j in tradesLive if j[0]>=str(x.min())]

        self.ax.plot(x, y, color="steelblue", label="Price", linewidth=0.6, alpha=0.8)
        if len(tradesLive)>0:
            buyTime= [pd.Timestamp(j[0]) for j in tradesLiveInterval if j[3]=="Buy"]
            buyPrice = [j[2] for j in tradesLiveInterval if j[3] == "Buy"]
            sellTime = [pd.Timestamp(j[0]) for j in tradesLiveInterval if j[3] == "Sell"]
            sellPrice = [j[2] for j in tradesLiveInterval if j[3] == "Sell"]
            self.ax.scatter(np.array(buyTime), buyPrice,  marker="^", color="g", s=30, label="Buy")
            self.ax.scatter(np.array(sellTime), sellPrice, marker="v", color="r", s=30, label="Sell")
        self.ax.tick_params(axis="x", labelsize=10, colors="#b3d9ff")
        self.ax.tick_params(axis="y", labelsize=10, colors="#b3d9ff")
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
        locator = MaxNLocator(prune='both', nbins=10, n=10)
        self.ax.xaxis.set_major_locator(locator)
        for tick in self.ax.get_xticklabels():
            tick.set_rotation(30)

        self.ax.grid(True)
        self.ax.grid(linestyle="-", linewidth="0.2")
        self.ax.legend()
        pnlText= "LastPnl: "+str(round(lastTradePnl, 3)) + \
                 "\nTotalPnl: "+str(round(totalPnl, 3)) + \
                 "\nPercChange: "+str(round(percentChange, 3))
        plt.text(0.02, 0.85, pnlText, fontsize=9, transform=plt.gcf().transFigure, \
                 color="#b3d9ff",bbox=dict(facecolor='steelblue', alpha=0.3))
        plt.subplots_adjust(left=0.27)
        plt.pause(0.001)
        plt.draw()
