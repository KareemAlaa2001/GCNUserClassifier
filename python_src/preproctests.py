import datetime
import preprocessing
from preprocessing import sotimeToTimestamp

def testSoTimeToTimestamp():
    dttest = datetime(year=2005,month=10, day=3, hour=15, minute=59, second=59, microsecond=987000)
    tstamptest = datetime.timestamp(dttest)
    print(tstamptest)
    sotimetest = "2005-10-03T15:59:59.987"
    sotimestamp = sotimeToTimestamp(sotimetest)
    print(sotimestamp)
    if tstamptest == sotimestamp:
        print('it works')
    else:
        print('something went wrong')