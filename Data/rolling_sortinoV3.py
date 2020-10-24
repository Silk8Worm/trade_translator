def rolling_Sortino(port_vals, startingValue):

    MAR = 0
    annualReturns = []
    excessReturns = []
    negativeExcessReturns = []
    negativeExcessReturnsSqrd = []
    avgDailyReturn = 0
    RFR = 0
    excessReturn = 0
    downsideDev = 0
    sortino = 0



    if len(port_vals) <= 10:
        return None


    annualReturns.append((port_vals[0]-startingValue)/startingValue)

    for i in range(1, len(port_vals)):
        annualReturns.append((port_vals[i]-port_vals[i-1])/port_vals[i-1])

    for i in range(len(annualReturns)):
        excessReturns.append(annualReturns[i] - MAR)

    for i in range(len(excessReturns)):
        if excessReturns[i] > 0:
            negativeExcessReturns.append(0)
        else:
            negativeExcessReturns.append(excessReturns[i])

    for i in range (len(negativeExcessReturns)):
        negativeExcessReturnsSqrd.append(negativeExcessReturns[i]**2)

    avgDailyReturn = sum(annualReturns)/len(annualReturns)
    excessReturn = avgDailyReturn - RFR
    downsideDev = (sum(negativeExcessReturnsSqrd)/len(negativeExcessReturnsSqrd))**0.5

    if downsideDev == 0:
        return 100000

    sortino = avgDailyReturn/downsideDev

    return sortino
