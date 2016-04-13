from transliterate import translit
import urllib.request
import urllib.parse
import json
import re
import time


def main():
    input_string_values = input('Введите город, улицу, номер дома через запятую: ')
    test_data(input_string_values)


def test_data(input_string):
    # убрать пробелы и разбиты на состовляющие
    input_data = re.sub(' ', '', input_string).split(',')
    input_city = input_data[0]
    input_street = input_data[1]
    input_house_number = input_data[2]

    input_values = re.sub(' ', '', input_string)
    # транслитерация
    t_input_values = translit(input_values, 'ru', reversed=True)
    input_list = t_input_values.split(',')

    city = input_list[0]
    street = input_list[1]
    house_number = input_list[2]

    address = city+'/'+street+'/'+house_number
    q = address

    # get запрос к серверу для получения координат
    params = urllib.parse.urlencode({'format': 'json'})
    url = "http://nominatim.openstreetmap.org/search/{1}?{0}".format(params, q)
    print(url)
    req = urllib.request.Request(url, headers={'User-Agent': 'super'})
    _start_time = time.time()
    with urllib.request.urlopen(req) as res:
        time_1 = time.time() - _start_time
        print("Время выполнения GET запроса: {:.3f} с".format(time.time() - _start_time))
        j = json.loads(res.read().decode('utf-8'))
        try:
            lat = j[0]['lat']
            lon = j[0]['lon']
        except IndexError:
            print('Out of range')
        except Exception:
            print(Exception)

    params = urllib.parse.urlencode({'lat': lat, 'lon': lon, 'format': 'json'})
    url = "http://nominatim.openstreetmap.org/reverse?%s" % params
    print(url)

    # get запрос к сервену для поллучения адреса
    req = urllib.request.Request(url, headers={'User-Agent': 'super'})
    _start_time = time.time()
    with urllib.request.urlopen(req) as f:
        time_2 = time.time() - _start_time
        print("Время выполнения GET запроса: {:.3f} с".format(time.time() - _start_time))
        j = json.loads(f.read().decode('utf-8'))
        address = j['address']
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
    print('Город: '+input_city)
    print('Улица: '+input_street)
    print('Номер дома: '+input_house_number)

    return [new_city, new_street, new_house_number, input_city, input_street, input_house_number, round(time_1, 3),
            round(time_2, 3)]


if __name__ == "__main__":
   main()