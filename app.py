from flask import Flask, request

import service

app = Flask(__name__)


@app.route('/api/file/edf', methods=['GET', 'POST'])
def upload_edf_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "Файл не загружен", 400

        if "first_name" not in request.form \
                or "last_name" not in request.form \
                or "gender" not in request.form \
                or "age" not in request.form:
            return "Отсутствует информация о пациенте", 400

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        age = request.form['age']
        date_start = None
        if "date_start" in request.form:
            date_start = request.form['date_start']

        file = request.files['file']
        service.detect_and_save_edf(file, first_name, last_name, gender, age, date_start)

        return "OK", 200

    return "Загрузка файла не поддерживает метод GET", 400


@app.route('/api/file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        print(file)

    return 'OK'


if __name__ == '__main__':
    app.run()
