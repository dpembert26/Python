import datetime
curdate = datetime.datetime.strptime("Thursday 21 March 1985" , "%A %d %B %Y" )


def gettime():
    print("Please attend the party on %s" % curdate.strftime("%A %dth %B %Y"))


def main():
    gettime()

main()