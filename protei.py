from flask import Flask, render_template, request, redirect
from app import app as app_console

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    return render_template('home.html', result=0)


@app.route('/', methods=['POST'])
def get_data():
    output_list = app_console.test_data(request.form['city']+','+request.form['street']+','+request.form['house_number'])
    return render_template('home.html', result=1, new_city=output_list[0], new_street=output_list[1],
                    new_number=output_list[2], old_city=output_list[3], old_street=output_list[4],
                    old_number=output_list[5], time_1=output_list[6], time_2=output_list[7])


if __name__ == '__main__':
    app.run()
