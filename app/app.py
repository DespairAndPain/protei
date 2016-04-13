from transliterate import translit
import urllib.request
import urllib.parse
import json
import re
import time


input_values = input('Введите город, улицу, номер дома через запятую: ')
print(input_values)

input_values = re.sub(' ', '', input_values)
t_input_values = translit(input_values, 'ru', reversed=True)
input_list = t_input_values.split(',')
print(input_list)
city = input_list[0]
street = input_list[1]
house_number = input_list[2]

address = city+'/'+street+'/'+house_number
q = address

params = urllib.parse.urlencode({'format': 'json'})
url = "http://nominatim.openstreetmap.org/search/{1}?{0}".format(params, q)
print(url)
req = urllib.request.Request(url, headers={'User-Agent': 'super'})
_start_time = time.time()
with urllib.request.urlopen(req) as res:
    print("Время выполнения GET запроса: {:.3f} с".format(time.time() - _start_time))
    j = json.loads(res.read().decode('utf-8'))
    lat = j[0]['lat']
    lon = j[0]['lon']
    print(j)


params = urllib.parse.urlencode({'lat': lat, 'lon': lon, 'format': 'json'})
url = "http://nominatim.openstreetmap.org/reverse?%s" % params
print(url)

req = urllib.request.Request(url, headers={'User-Agent': 'super'})
_start_time = time.time()
with urllib.request.urlopen(req) as f:
    print("Время выполнения GET запроса: {:.3f} с".format(time.time() - _start_time))
    j = json.loads(f.read().decode('utf-8'))
    address = j.get('address')
    new_house_number = address['house_number']
    new_street = address['road']
    new_city = address['city']

print('=====================')
print('Адрес полученный:')
print('Город: '+new_city)
print('Улица: '+new_street)
print('Номер дома: '+new_house_number)
print('=====================')
print('Адрес заданный:')
print('Город: '+city)
print('Улица: '+street)
print('Номер дома: '+house_number)