import datetime
# import preprocessing
from extraction import extractAttribList, recentUsers
# from preprocessing import sotimeToTimestamp

# def testSoTimeToTimestamp():
#     dttest = datetime(year=2005,month=10, day=3, hour=15, minute=59, second=59, microsecond=987000)
#     tstamptest = datetime.timestamp(dttest)
#     print(tstamptest)
#     sotimetest = "2005-10-03T15:59:59.987"
#     sotimestamp = sotimeToTimestamp(sotimetest)
#     print(sotimestamp)
#     if tstamptest == sotimestamp:
#         print('it works')
#     else:
#         print('something went wrong')



# success
def testExtractAttribList():
    getViews = lambda user: user.get('Views')

    ten_recent_user_views = list(map(getViews, recentUsers[:10]))
    print(ten_recent_user_views)

    extractedViews = extractAttribList(recentUsers[:10], 'Views')
    print(extractedViews)
    assert ten_recent_user_views == extractedViews, "Extractedviews and first 10 user views are not equal!" 

def main():
    # main function in which tests can be run
    testExtractAttribList()

if __name__ == '__main__':
    main()
