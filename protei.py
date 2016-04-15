from flask import Flask, render_template, request, redirect
from app import app as app_console
import os
import glob

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'static')
UPLOAD_FOLDER = APP_STATIC+'/test_data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def hello_world():
    return render_template('home.html', result=0)


@app.route('/', methods=['POST'])
def get_data():
    # удалить все данные из временного каталога
    files = glob.glob(UPLOAD_FOLDER+'/*')
    for f in files:
        os.remove(f)

    # по имени с input взять файлы и сохранить во временный каталог
    files = request.files.getlist('file[]')
    if files:
        for file in files:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    list_results = []
    for root, dirs, files in os.walk(UPLOAD_FOLDER):
        list_results.append([files, app_console.main(files)])
    print(list_results)
    return render_template('home.html', result=1, items=list_results)


if __name__ == '__main__':
    app.run()
