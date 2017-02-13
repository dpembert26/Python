import sys

try:
    area = 0/0
except:
    errors = sys.exc_info()
    for idx, error in enumerate(errors):
        if idx < 2:
            print(error)
