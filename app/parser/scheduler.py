import schedule
import time
from app.parser.parser import parseAllEconomist
from app.parser.parser import parseNewEconomist
import sys


def ParseSources():
    parseNewEconomist()


schedule.every(1).minutes.do(ParseSources)


if __name__ == "main":
    if sys.argv[1] == 'parse_all':
        parseAllEconomist()

    while True:
        schedule.run_pending()
        time.sleep(1)
        print('sleep...')
