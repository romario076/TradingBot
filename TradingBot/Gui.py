
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
import test_support
import datetime
from BotGetData import BotGetData
from botstrategy import BotStrategy
from botChart import botChart
from botlog import BotLog
from AutoScroll import *
import matplotlib.pyplot as plt
import colorama
import crayons
import warnings
warnings.filterwarnings("ignore")
colorama.init()

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = Tk()
    top = Trading_Gui (root)
    test_support.init(root, top)
    root.mainloop()

w = None
def create_Trading_Gui(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel (root)
    top = Trading_Gui (w)
    test_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Trading_Gui():
    global w
    w.destroy()
    w = None

def chartHorizon(histDataUpdated, interval):
    currentTime= histDataUpdated.Date.iloc[-1]
    histDataUpdated= histDataUpdated[histDataUpdated.Date>=currentTime-datetime.timedelta(minutes=interval)]
    return histDataUpdated


class Trading_Gui:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#d9d9d9' # X11 color: 'gray85'
        self.root = root
        self.style = ttk.Style()
        self.style.theme_use("vista")
        #if sys.platform == "win32":
        #    self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background= [('selected', _compcolor), ('active',_ana2color)])
        self.showChart = False
        self.startTrading = False
        self.closeAll= False
        self.stopRunning= False
        self.numberOfExecutions= 0
        self.numberOfTrades = 0
        self.output = BotLog()
        self.liveChartObject= []
        self.CheckVar = IntVar()

        top.geometry("990x518+446+155")
        top.title("Trading Gui")
        top.configure(background="#d9d9d9")

        self.TFrame1 = ttk.Frame(top)
        self.TFrame1.place(relx=0.01, rely=0.02, relheight=0.98, relwidth=0.11)
        self.TFrame1.configure(relief=GROOVE)
        self.TFrame1.configure(borderwidth="2")
        self.TFrame1.configure(relief=GROOVE)
        self.TFrame1.configure(width=95)

        self.Run = ttk.Button(self.TFrame1, command=self.main)
        self.Run.place(relx=0.11, rely=0.07, height=35, width=76)
        self.Run.configure(takefocus="")
        self.Run.configure(text='''Run''')
        self.Run.configure(width=76)

        self.Stop = ttk.Button(self.TFrame1, command=self.stopRun)
        self.Stop.place(relx=0.11, rely=0.17, height=35, width=76)
        self.Stop.configure(takefocus="")
        self.Stop.configure(text='''Stop''')
        self.Stop.configure(width=76)

        self.StartTrade = ttk.Button(self.TFrame1, command= self.useStartegy)
        self.StartTrade.place(relx=0.11, rely=0.27, height=35, width=76)
        self.StartTrade.configure(takefocus="")
        self.StartTrade.configure(text='''StartTrade''')
        self.StartTrade.configure(width=76)

        self.StopTrade = ttk.Button(self.TFrame1, command=self.stopTrade)
        self.StopTrade.place(relx=0.11, rely=0.37, height=35, width=76)
        self.StopTrade.configure(takefocus="")
        self.StopTrade.configure(text='''StopTrade''')
        self.StopTrade.configure(width=76)

        self.ShowChart = ttk.Button(self.TFrame1, command= self.chartOpen)
        self.ShowChart.place(relx=0.11, rely=0.47, height=35, width=76)
        self.ShowChart.configure(takefocus="")
        self.ShowChart.configure(text='''ShowChart''')
        self.ShowChart.configure(width=76)

        self.CloseChart = ttk.Button(self.TFrame1, command= self.chartClose)
        self.CloseChart.place(relx=0.11, rely=0.57, height=35, width=76)
        self.CloseChart.configure(takefocus="")
        self.CloseChart.configure(text='''CloseChart''')
        self.CloseChart.configure(width=76)

        self.ClosePos = ttk.Button(self.TFrame1, command= self.closeAllPositions)
        self.ClosePos.place(relx=0.11, rely=0.67, height=35, width=76)
        self.ClosePos.configure(takefocus="")
        self.ClosePos.configure(text='''ClosePos''')

        self.CheckVar.set(1)
        self.SaveTrades = Checkbutton(self.TFrame1, text="SaveHistory", variable=self.CheckVar, bg=_bgcolor)
        self.SaveTrades.place(relx=0.11, rely=0.77, height=35, width=80)

        self.Exit = ttk.Button(self.TFrame1, command= self.CloseWindow)
        self.Exit.place(relx=0.11, rely=0.9, height=35, width=76)
        self.Exit.configure(takefocus="")
        self.Exit.configure(text='''Exit''')
        self.Exit.configure(width=76)

        self.TFrame3 = Frame(top)
        self.TFrame3.place(relx=0.15, rely=0.05, relheight=0.1, relwidth=0.8)
        self.TFrame3.configure(relief=GROOVE)
        self.TFrame3.configure(borderwidth="2")
        self.TFrame3.configure(relief=GROOVE)
        self.TFrame3.configure(width=475)
        self.TFrame3.configure(takefocus="0")

        self.TLabel5 = Label(self.TFrame3)
        self.TLabel5.place(relx=0.01, rely=0.18, height=19, width=55)
        self.TLabel5.configure(font=('Helvetica', 8))
        self.TLabel5.configure(foreground="#075bb8")
        self.TLabel5.configure(relief=FLAT)
        self.TLabel5.configure(text='''Ticker:''')

        self.ticker = Entry(self.TFrame3)
        self.ticker.insert(END, str("USDT_BTC"))
        self.ticker.place(relx=0.07, rely=0.18, relheight=0.44, relwidth=0.09)
        self.ticker.configure(font=('Helvetica', 10))
        self.ticker.configure(background="white")
        self.ticker.configure(font="TkTextFont")
        self.ticker.configure(foreground="black")
        self.ticker.configure(highlightbackground="#d9d9d9")
        self.ticker.configure(highlightcolor="black")
        self.ticker.configure(insertbackground="black")
        self.ticker.configure(selectbackground="#c4c4c4")
        self.ticker.configure(selectforeground="black")
        self.ticker.configure(takefocus="0")

        self.TLabel4 = Label(self.TFrame3)
        self.TLabel4.place(relx=0.19, rely=0.18, height=19, width=75)
        self.TLabel4.configure(font=('Helvetica', 8))
        self.TLabel4.configure(foreground="#075bb8")
        self.TLabel4.configure(relief=FLAT)
        self.TLabel4.configure(text='''StopLossEdge:''')

        self.StopLossEdge = Entry(self.TFrame3)
        self.StopLossEdge.insert(END, str(10))
        self.StopLossEdge.place(relx=0.29, rely=0.18, relheight=0.44, relwidth=0.09)
        self.StopLossEdge.configure(font=('Helvetica', 10))
        self.StopLossEdge.configure(background="white")
        self.StopLossEdge.configure(font="TkTextFont")
        self.StopLossEdge.configure(foreground="black")
        self.StopLossEdge.configure(highlightbackground="#d9d9d9")
        self.StopLossEdge.configure(highlightcolor="black")
        self.StopLossEdge.configure(insertbackground="black")
        self.StopLossEdge.configure(selectbackground="#c4c4c4")
        self.StopLossEdge.configure(selectforeground="black")
        self.StopLossEdge.configure(takefocus="0")

        self.TLabel5 = Label(self.TFrame3)
        self.TLabel5.place(relx=0.41, rely=0.2, height=19, width=65)
        self.TLabel5.configure(font=('Helvetica', 8))
        self.TLabel5.configure(foreground="#075bb8")
        self.TLabel5.configure(relief=FLAT)
        self.TLabel5.configure(takefocus="0")
        self.TLabel5.configure(text='''EntryEdge:''')

        self.EntryEdge = Entry(self.TFrame3)
        self.EntryEdge.insert(END, str(0))
        self.EntryEdge.place(relx=0.49, rely=0.15, relheight=0.44, relwidth=0.09)
        self.EntryEdge.configure(background="white")
        self.EntryEdge.configure(font="TkTextFont")
        self.EntryEdge.configure(foreground="black")
        self.EntryEdge.configure(highlightbackground="#d9d9d9")
        self.EntryEdge.configure(highlightcolor="black")
        self.EntryEdge.configure(insertbackground="black")
        self.EntryEdge.configure(selectbackground="#c4c4c4")
        self.EntryEdge.configure(selectforeground="black")
        self.EntryEdge.configure(takefocus="0")

        self.TLabel6 = Label(self.TFrame3)
        self.TLabel6.place(relx=0.62, rely=0.2, height=19, width=85)
        self.TLabel6.configure(font=('Helvetica', 8))
        self.TLabel6.configure(foreground="#075bb8")
        self.TLabel6.configure(relief=FLAT)
        self.TLabel6.configure(takefocus="0")
        self.TLabel6.configure(text='''OpenTradesLimit:''')

        self.OpenTradesLimit = Entry(self.TFrame3)
        self.OpenTradesLimit.insert(END, str(4))
        self.OpenTradesLimit.place(relx=0.73, rely=0.15, relheight=0.44, relwidth=0.09)
        self.OpenTradesLimit.configure(background="white")
        self.OpenTradesLimit.configure(font="TkTextFont")
        self.OpenTradesLimit.configure(foreground="black")
        self.OpenTradesLimit.configure(highlightbackground="#d9d9d9")
        self.OpenTradesLimit.configure(highlightcolor="black")
        self.OpenTradesLimit.configure(insertbackground="black")
        self.OpenTradesLimit.configure(selectbackground="#c4c4c4")
        self.OpenTradesLimit.configure(selectforeground="black")
        self.OpenTradesLimit.configure(takefocus="0")


        self.style.configure('Treeview.Heading',  font="TkDefaultFont")
        self.Scrolledtreeview1 = ScrolledTreeView(top)
        self.Scrolledtreeview1.place(relx=0.15, rely=0.23, relheight=0.28, relwidth=0.6)
        self.Scrolledtreeview1.configure(columns="Col1 Col2 Col3 Col4 Col5")
        self.Scrolledtreeview1.configure(takefocus="0")
        self.Scrolledtreeview1.heading("#0",text="Id")
        self.Scrolledtreeview1.heading("#0",anchor="center")
        self.Scrolledtreeview1.column("#0",width="35")
        self.Scrolledtreeview1.column("#0",minwidth="20")
        self.Scrolledtreeview1.column("#0",stretch="1")
        self.Scrolledtreeview1.column("#0",anchor="w")
        self.Scrolledtreeview1.heading("Col1",text="Time")
        self.Scrolledtreeview1.heading("Col1",anchor="center")
        self.Scrolledtreeview1.column("Col1",width="150")
        self.Scrolledtreeview1.column("Col1",minwidth="20")
        self.Scrolledtreeview1.column("Col1",stretch="1")
        self.Scrolledtreeview1.column("Col1",anchor="w")
        self.Scrolledtreeview1.heading("Col2",text="Symbol")
        self.Scrolledtreeview1.heading("Col2",anchor="center")
        self.Scrolledtreeview1.column("Col2",width="80")
        self.Scrolledtreeview1.column("Col2",minwidth="20")
        self.Scrolledtreeview1.column("Col2",stretch="1")
        self.Scrolledtreeview1.column("Col2",anchor="w")
        self.Scrolledtreeview1.heading("Col3",text="Side")
        self.Scrolledtreeview1.heading("Col3",anchor="center")
        self.Scrolledtreeview1.column("Col3",width="80")
        self.Scrolledtreeview1.column("Col3",minwidth="20")
        self.Scrolledtreeview1.column("Col3",stretch="1")
        self.Scrolledtreeview1.column("Col3",anchor="w")
        self.Scrolledtreeview1.heading("Col4",text="Price")
        self.Scrolledtreeview1.heading("Col4",anchor="center")
        self.Scrolledtreeview1.column("Col4",width="80")
        self.Scrolledtreeview1.column("Col4",minwidth="20")
        self.Scrolledtreeview1.column("Col4",stretch="1")
        self.Scrolledtreeview1.column("Col4",anchor="w")
        self.Scrolledtreeview1.heading("Col5",text="Pnl")
        self.Scrolledtreeview1.heading("Col5",anchor="center")
        self.Scrolledtreeview1.column("Col5",width="80")
        self.Scrolledtreeview1.column("Col5",minwidth="20")
        self.Scrolledtreeview1.column("Col5",stretch="1")
        self.Scrolledtreeview1.column("Col5",anchor="w")


        self.menubar = Menu(top,font="TkMenuFont",bg='#bef7bb',fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.Scrolledtreeview2 = ScrolledTreeView(top)
        self.style.configure("Scrolledtreeview2", font='helvetica 24')
        self.Scrolledtreeview2.place(relx=0.15, rely=0.61, relheight=0.32, relwidth=0.8)
        self.Scrolledtreeview2.configure(columns="Col1 Col2 Col3 Col4 Col5 Col6 Col7")
        self.Scrolledtreeview2.configure(takefocus="0")
        self.Scrolledtreeview2.heading("#0", text="Id")
        self.Scrolledtreeview2.heading("#0", anchor="center")
        self.Scrolledtreeview2.column("#0", width="35")
        self.Scrolledtreeview2.column("#0", minwidth="20")
        self.Scrolledtreeview2.column("#0", stretch="1")
        self.Scrolledtreeview2.column("#0", anchor="w")
        self.Scrolledtreeview2.heading("Col1", text="EntryTime")
        self.Scrolledtreeview2.heading("Col1", anchor="center")
        self.Scrolledtreeview2.column("Col1", width="150")
        self.Scrolledtreeview2.column("Col1", minwidth="20")
        self.Scrolledtreeview2.column("Col1", stretch="1")
        self.Scrolledtreeview2.column("Col1", anchor="w")
        self.Scrolledtreeview2.heading("Col2", text="ExitTime")
        self.Scrolledtreeview2.heading("Col2", anchor="center")
        self.Scrolledtreeview2.column("Col2", width="150")
        self.Scrolledtreeview2.column("Col2", minwidth="20")
        self.Scrolledtreeview2.column("Col2", stretch="1")
        self.Scrolledtreeview2.column("Col2", anchor="w")
        self.Scrolledtreeview2.heading("Col3", text="Symbol")
        self.Scrolledtreeview2.heading("Col3", anchor="center")
        self.Scrolledtreeview2.column("Col3", width="81")
        self.Scrolledtreeview2.column("Col3", minwidth="20")
        self.Scrolledtreeview2.column("Col3", stretch="1")
        self.Scrolledtreeview2.column("Col3", anchor="w")
        self.Scrolledtreeview2.heading("Col4", text="Side")
        self.Scrolledtreeview2.heading("Col4", anchor="center")
        self.Scrolledtreeview2.column("Col4", width="80")
        self.Scrolledtreeview2.column("Col4", minwidth="20")
        self.Scrolledtreeview2.column("Col4", stretch="1")
        self.Scrolledtreeview2.column("Col4", anchor="w")
        self.Scrolledtreeview2.heading("Col5", text="EntryPrice")
        self.Scrolledtreeview2.heading("Col5", anchor="center")
        self.Scrolledtreeview2.column("Col5", width="80")
        self.Scrolledtreeview2.column("Col5", minwidth="20")
        self.Scrolledtreeview2.column("Col5", stretch="1")
        self.Scrolledtreeview2.column("Col5", anchor="w")
        self.Scrolledtreeview2.heading("Col6", text="ExitPrice")
        self.Scrolledtreeview2.heading("Col6", anchor="center")
        self.Scrolledtreeview2.column("Col6", width="80")
        self.Scrolledtreeview2.column("Col6", minwidth="20")
        self.Scrolledtreeview2.column("Col6", stretch="1")
        self.Scrolledtreeview2.column("Col6", anchor="w")
        self.Scrolledtreeview2.heading("Col7", text="Pnl")
        self.Scrolledtreeview2.heading("Col7", anchor="center")
        self.Scrolledtreeview2.column("Col7", width="80")
        self.Scrolledtreeview2.column("Col7", minwidth="20")
        self.Scrolledtreeview2.column("Col7", stretch="1")
        self.Scrolledtreeview2.column("Col7", anchor="w")

        self.Label1 = Label(top)
        self.Label1.place(relx=0.15, rely=0.17, height=25, width=595)
        self.Label1.configure(font=('Helvetica', 10))
        self.Label1.configure(anchor=N)
        self.Label1.configure(background="#b4c2fe")
        self.Label1.configure(compound="left")
        self.Label1.configure(cursor="bottom_left_corner")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(justify=LEFT)
        self.Label1.configure(relief=RIDGE)
        self.Label1.configure(text='''Opened Positions''')
        self.Label1.configure(textvariable=test_support)
        self.Label1.configure(width=459)

        self.Label2 = Label(top)
        self.Label2.place(relx=0.15, rely=0.55, height=25, width=788)
        self.Label2.configure(font=('Helvetica', 10))
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(activeforeground="black")
        self.Label2.configure(anchor=N)
        self.Label2.configure(background="#b4c2fe")
        self.Label2.configure(compound="left")
        self.Label2.configure(cursor="bottom_left_corner")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(highlightbackground="#d9d9d9")
        self.Label2.configure(highlightcolor="black")
        self.Label2.configure(justify=LEFT)
        self.Label2.configure(relief=RIDGE)
        self.Label2.configure(text='''Trades''')
        self.Label2.configure(width=459)

        self.TFrame2 = Frame(top)
        self.TFrame2.place(relx=0.76, rely=0.23, relheight=0.22, relwidth=0.2)
        self.TFrame2.configure(relief=SUNKEN)
        self.TFrame2.configure(borderwidth="2")
        self.TFrame2.configure(relief=SUNKEN)
        self.TFrame2.configure(width=150)
        self.TFrame2.configure(takefocus="0")

        self.TotalPnl = Label(self.TFrame2)
        self.TotalPnl.place(relx=0.002, rely=0.17, height=29, width=86)
        self.TotalPnl.configure(font=('Helvetica', 11))
        self.TotalPnl.configure(foreground="#075bb8")
        self.TotalPnl.configure(relief=FLAT)
        self.TotalPnl.configure(justify=RIGHT)
        self.TotalPnl.configure(takefocus="0")
        self.TotalPnl.configure(text='''TotalPnl:''')

        self.TradesCount = Label(self.TFrame2)
        self.TradesCount.place(relx=0.01, rely=0.63, height=29, width=106)
        self.TradesCount.configure(font=('Helvetica', 11))
        self.TradesCount.configure(foreground="#075bb8")
        self.TradesCount.configure(relief=FLAT)
        self.TradesCount.configure(justify=RIGHT)
        self.TradesCount.configure(takefocus="0")
        self.TradesCount.configure(text='''TradesCount:''')

        self.tradesCount = Text(self.TFrame2)
        self.tradesCount.configure(font=('Helvetica', 10))
        self.tradesCount.place(relx=0.52, rely=0.6, relheight=0.3, relwidth=0.4)
        self.tradesCount.configure(font=('Helvetica', 10))
        self.tradesCount.configure(background="white")
        self.tradesCount.configure(font="TkTextFont")
        self.tradesCount.configure(foreground="black")
        self.tradesCount.configure(highlightbackground="#d9d9d9")
        self.tradesCount.configure(highlightcolor="black")
        self.tradesCount.configure(insertbackground="black")
        self.tradesCount.configure(selectbackground="#c4c4c4")
        self.tradesCount.configure(selectforeground="black")
        self.tradesCount.configure(takefocus="0")
        self.tradesCount.configure(width=104)

        self.totalPnl = Text(self.TFrame2, font= ('Times', '24', 'bold italic') )
        self.totalPnl.place(relx=0.52, rely=0.1, relheight=0.3, relwidth=0.4)
        self.totalPnl.configure(font=('Helvetica', 10))
        self.totalPnl.configure(background="white")
        self.totalPnl.configure(font="TkTextFont")
        self.totalPnl.configure(foreground="black")
        self.totalPnl.configure(highlightbackground="#d9d9d9")
        self.totalPnl.configure(highlightcolor="black")
        self.totalPnl.configure(insertbackground="black")
        self.totalPnl.configure(selectbackground="#c4c4c4")
        self.totalPnl.configure(selectforeground="black")
        self.totalPnl.configure(takefocus="0")
        self.totalPnl.configure(width=104)


    def stopRun(self):
        self.root.update()
        self.stopRunning= True
        self.output.log(crayons.red("System stop.........."))

    def CloseWindow(self) :
        self.root.destroy()

    def chartOpen(self) :
        self.liveChartObject = botChart()
        self.root.update()
        self.showChart= True

    def chartClose(self) :
        self.root.update()
        self.showChart= False
        plt.close()

    def useStartegy(self) :
        self.root.update()
        self.startTrading= True
        self.stopRunning= False
        self.output.log(crayons.green("Start trading.........."))

    def stopTrade(self) :
        self.root.update()
        self.startTrading = False
        self.output.log(crayons.green("End trading.........."))

    def closeAllPositions(self) :
        self.root.update()
        self.closeAll = True

    def insertDataExecutions(self, executions):
        n= len(executions)
        if n>self.numberOfExecutions:
            newExecutions= executions[-(n-self.numberOfExecutions):]
            k= n
            for row in newExecutions:
                self.Scrolledtreeview1.insert('', 'end', text=str(k),\
                                  values=( str(row[0]).split(" ")[-1], row[1], row[3], round(row[2],2), round(row[4],3)))
                k= k+1
            self.numberOfExecutions= n


    def insertDataTrades(self, trades):
        n= len(trades)
        if n>self.numberOfTrades:
            newTrades= trades[-(n-self.numberOfTrades):]
            k= self.numberOfTrades
            for row in newTrades:
                self.Scrolledtreeview2.insert('', 'end', text=str(k),\
                                  values=( str(row[0]).split(" ")[-1], str(row[1]).split(" ")[-1], row[2], \
                                           row[5], round(row[3],2), round(row[4],2), round(row[6],3)))
                k= k+1
            self.numberOfTrades= n

    def insertOpenData(self, openedPositions):
        self.Scrolledtreeview1.delete(*self.Scrolledtreeview1.get_children())
        for i,row in enumerate(openedPositions):
            self.Scrolledtreeview1.insert('', 'end', text=str(i),\
                                values=( str(row[0]).split(" ")[-1],  row[1], \
                                       row[2], round(row[3], 2), round(row[4], 2)), tags=('new'))

    def saveTradeHistory(self, strategy):
        if self.CheckVar:
            data= strategy.showExecutions()
            if len(data)>0:
                data.to_csv("TradingHistory.csv", index=False)
            else:
                with open("TradingHistory.csv", 'w'):
                    pass


    def main(self):
        period = 10
        pair = "USDT_BTC"
        lengthMA = 50
        error=False
        self.stopRunning= False
        try:
            data = BotGetData(pair, period)
        except Exception as e:
            messagebox.showinfo("Error", e)
            error= True
        try:
            stopLossEdge= float(self.StopLossEdge.get())
        except:
            messagebox.showinfo("Error", "Wrong StopLoss input. Must be integer.")
            error= True
        try:
            entryEdge= float(self.EntryEdge.get())
            entryEdge= 0
        except:
            messagebox.showinfo("Error", "Wrong StopLoss input. Must be numeric.")
            error= True
        try:
            openPosLimit= int(self.OpenTradesLimit.get())
            if openPosLimit<=0:
                messagebox.showinfo("Error", "Wrong openPosLimit input. Must be integer>0.")
        except:
            messagebox.showinfo("Error", "Wrong openPosLimit input. Must be integer.")
            error= True
        try:
            historical = data.historicalData
        except:
            messagebox.showinfo("Error", "Could`t get data from Poloniex!")
            historical= []
            error= True
        if not error:
            prices = historical.Price.tolist()
            if (len(historical) > lengthMA):
                prices = prices[-lengthMA:]
            else:
                print("Not enough historical data for MA=" + str(lengthMA))
                lengthMA = len(prices)

            strategy = BotStrategy(prices=prices, pair=pair, lengthMA=lengthMA, \
                                   openPosLimit=openPosLimit, stopLossEdge=stopLossEdge, entryEdge=entryEdge)

            while True:
                try:
                    if self.stopRunning:
                        self.saveTradeHistory(strategy=strategy)
                        break
                    data.updateData()
                    lastPairPrice = data.lastPrice
                    prices.append(lastPairPrice)
                    prices = prices[-lengthMA:]
                    strategy.tick(lastPairPrice, self.startTrading)
                    executions = strategy.allExecutions.execData
                    trades = strategy.allTrades.tradesData
                    histDataUpdated = chartHorizon(histDataUpdated=data.historicalData, interval=15)
                    openedPositions= strategy.openedPositions
                    self.insertDataTrades(trades)
                    self.insertOpenData(openedPositions)
                    self.tradesCount.delete(1.0, END)
                    self.tradesCount.insert(END, str(len(trades)))
                    self.totalPnl.delete(1.0, END)
                    self.totalPnl.insert(END, str(round(strategy.totalPnl,1)))
                    if self.closeAll:
                        strategy.closeAll()
                        self.saveTradeHistory(strategy=strategy)
                    if self.showChart:
                        self.liveChartObject.botLiveChart(x=histDataUpdated.Date, y=histDataUpdated.Price, \
                                            tradesLive=executions, lastTradePnl=strategy.lastTradePnl, \
                                            totalPnl=strategy.totalPnl, percentChange=data.percentChange)
                    self.root.update()

                except Exception as e:
                    messagebox.showinfo("Error", str(e))
                    strategy.closeAll()
                    self.saveTradeHistory(strategy=strategy)
                    break


vp_start_gui()
