from typing import List
import numpy
import math


def rolling_sharpe(port_vals: List[float], starting: float) -> float:
    """
    It does what the spreadsheet does, so if the spreadsheet can do it, so can
    this.

    >>> rolling_sharpe([100, 100.2, 100.5, 100.4, 100.2, 100.21, 99.21, 100, 100.8, 99.79, 100.79, 100.45, 100.84, 100.4, 100.89], 100)
    """

    RFR = .02
    D_RFR = (math.pow((1+RFR), (4/365))-1)
    daily_r = []
    avg_r_ann = []
    st_dev_ann = []

    if len(port_vals) <= 10:
        return None

    daily_r.append((port_vals[0]-starting)/starting)

    for i in range(1, len(port_vals)):
        daily_r.append((port_vals[i]-port_vals[i-1])/port_vals[i-1])

    for i in range(9, len(port_vals)):
        avg_r_ann.append(numpy.mean(daily_r[0:i+1])*252)

    for i in range(9, len(port_vals)):
        st_dev_ann.append(numpy.std(daily_r[0:i+1], ddof=1)*math.sqrt(252))

    if st_dev_ann[-1] == 0:
        return 0

    return (avg_r_ann[-1]-D_RFR)/st_dev_ann[-1]










