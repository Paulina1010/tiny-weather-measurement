import json
import urllib.request
import sys


url = 'https://api.meteo.pl/api/v1/model/coamps/grid/2a/coordinates/130,111/field/airtmp_zht_fcstfld/level/000002_000000/date/2017-11-11T00/forecast/'
headers = {"Authorization": "Token %s" % sys.argv[1]}
req = urllib.request.Request(url, headers=headers, method="POST")
with urllib.request.urlopen(req) as f:
    data = json.load(f)
    print(data)
