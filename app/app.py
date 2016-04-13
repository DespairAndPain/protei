import urllib.request
import urllib.parse
import json

street = 'dekabristov'
house_number = "30"
city = 'ekaterinburg'
address = city+'/'+street+'/'+house_number
q = address

params = urllib.parse.urlencode({'format': 'json'})
url = "http://nominatim.openstreetmap.org/search/{1}?{0}".format(params, q)
print(url)
req = urllib.request.Request(url, headers={'User-Agent': 'super'})
with urllib.request.urlopen(req) as res:
    j = json.loads(res.read().decode('utf-8'))
    lat = j[0]['lat']
    lon = j[0]['lon']
    #lat = res.get('lat')
    #lon = f[0]['lon']
    print(j)

params = urllib.parse.urlencode({'lat': lat, 'lon': lon, 'format': 'json'})
url = "http://nominatim.openstreetmap.org/reverse?%s" % params
print(url)
req = urllib.request.Request(url, headers={'User-Agent': 'super'})
with urllib.request.urlopen(req) as f:
    j = json.loads(f.read().decode('utf-8'))
    adress = j.get('address')
    house_number = adress['house_number']
    street = adress['road']

    print(j)