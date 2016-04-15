from transliterate import translit
import urllib.request
import urllib.parse
import json
import time
import xlrd
import os


def main(file_name):
    result = []

    file_path = os.path.dirname(os.path.abspath(__file__))+'/../static/test_data/'+file_name[0]
    rb = xlrd.open_workbook(file_path, formatting_info=True)
    sheet = rb.sheet_by_index(0)

    for rownum in range(sheet.nrows):
        row = sheet.row_values(rownum)
        if row[0] in range(1, 100, 1):
            result.append(test_data(row))
    print(result)
    for i in result:
        print('==========')
        print('ID теста: '+str(int(i[0])))
        print('Статус выполнения: ' + i[1])
        print('Время отклика сервера адрес>>координаты: ' + str(i[2]))
        print('Время отклика сервера координаты>>адрес: ' + str(i[3]))
    return result


def test_data(input_list):

    city = translit(input_list[1], 'ru', reversed=True)
    street = translit(input_list[2], 'ru', reversed=True)
    house_number = str(int(input_list[3]))

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
        if len(j) == 0:
            return [input_list[0], 'Null response on step 1']

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
        if len(j) == 0:
            return [input_list[0], 'Null response on step 2']

    if new_city == input_list[4] and new_street == input_list[5] and int(new_house_number) == int(input_list[6]):
        result_status = 'done'
    else:
        result_status = 'Wrong response'

    result = [input_list[0], result_status, round(time_1, 3), round(time_2, 3)]
    return result



if __name__ == "__main__":
   main(['test_data.xls'])