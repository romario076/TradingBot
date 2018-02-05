import numpy as np


class botMetrics(object):
    def __init__(self):
        pass

    def movingAverage(self, data, period):
        ma= 0
        if len(data)> 1:
            ma= sum(data[-period:])/len(data[-period:])
        return(ma)

    def momentum(self, dataPoints, period=14):
        if (len(dataPoints) > period - 1):
            return dataPoints[-1] * 100 / dataPoints[-period]

    def EMA(self, prices, period):
        x = np.asarray(prices)
        if period>len(x):
            period=len(x)
        weights = None
        weights = np.exp(np.linspace(-1., 0., period))
        weights /= weights.sum()

        dd= sum([a*b for a,b in zip(weights,x[-period:])])
        return dd

    def EMA2(self, prices, period):
        s = np.array(prices)
        n = period
        if len(s)<n:
            n=len(s)-1
        ema = []
        result=0
        j = 1

        # get n sma first and calculate the next n period ema
        sma = sum(s[:n]) / n
        multiplier = 2 / float(1 + n)
        ema.append(sma)

        # EMA(current) = ( (Price(current) - EMA(prev) ) x Multiplier) + EMA(prev)
        ema.append(((s[n] - sma) * multiplier) + sma)

        # now calculate the rest of the values
        for i in s[n + 1:]:
            tmp = ((i - ema[j]) * multiplier) + ema[j]
            j = j + 1
            ema.append(tmp)
        if len(ema)>0:
            result= ema[0]

        return result


    def MACD(self, prices, nslow=26, nfast=12):
        emaslow = self.EMA(prices, nslow)
        emafast = self.EMA(prices, nfast)
        return emaslow, emafast

    def RSI(self, prices, period=14):
        deltas = np.diff(prices)
        seed = deltas[:period + 1]
        up = seed[seed >= 0].sum() / period
        down = -seed[seed < 0].sum() / period
        rs = up / down
        rsi = np.zeros_like(prices)
        rsi[:period] = 100. - 100. / (1. + rs)

        for i in range(period, len(prices)):
            delta = deltas[i - 1]  # cause the diff is 1 shorter
            if delta > 0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta

            up = (up * (period - 1) + upval) / period
            down = (down * (period - 1) + downval) / period
            rs = up / down
            rsi[i] = 100. - 100. / (1. + rs)
        if len(prices) > period:
            return rsi[-1]
        else:
            return 50  # output a neutral amount until enough prices in list to calculate RSI