from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from jinja2 import Template

import config as config

# инициализация и подключение к бд
app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)


# роут на главную, выводит все сборки
@app.route('/', methods=['GET', 'POST'])
def index():
    # импортируем модель сборки, потому что в ней импортируется bd => выше поднять не можем
    from models import Musicset, Track
    search = request.args.get('search')
    select = request.args.get('select')

    if search:
        if select == 'artist':
            result = Track.query.filter(Track.artist.ilike('%{0}%'.format(search)))
        elif select == 'track_title':
            result = Track.query.filter(Track.title.ilike('%{0}%'.format(search)))
        elif select == 'set_title':
            mst = Musicset.query.filter(Musicset.set_title.ilike('%{0}%'.format(search)))
            result = []
            for item in mst:
                # скорее всего буедт баг, и надо почекать будет
                # ибо после каждой итерации result будет перезаписываться
                id = str(item.id)
                result.extend(Track.query.filter_by(set_id=id))
    else:
        # достаем ве записи
        result = Track.query.all()
    # if request.method == 'POST':
    #     pass
    # if request.method == 'GET':
    #     pass

    # возвращаем темплейт чтобы вывести заиси
    return render_template('start.html', mst=result)
    # return jsonify([p.to_dict() for p in track])


# роут для вывода, на вход /поле_для_поиска/значение
@app.route('/musicset/<path:val>', methods=['GET', 'POST'])
def musicset_search(val):
    # импортируем модель
    from models import Musicset
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        # режем поле по '/' первое значение поле, второе значение
        vals_to_search = val.split('/', maxsplit=1)
        # выбор поля по которому будет идти фильтрация, фильтрация + минимальные проверки
        if len(vals_to_search) != 2:
            return 'entered not true value'
        elif vals_to_search[0] == 'id':
            result = Musicset.query.filter_by(id=vals_to_search[1])
        elif vals_to_search[0] == 'set_title':
            result = Musicset.query.filter_by(set_title=vals_to_search[1])
        elif vals_to_search[0] == 'set_link':
            result = Musicset.query.filter_by(set_link=vals_to_search[1])
        elif vals_to_search[0] == 'set_tracks':
            result = Musicset.query.filter_by(set_tracks=vals_to_search[1])
        elif vals_to_search[0]:
            return 'check fields that you entered'
        # шаблон для вывода массива записей
        result_form = Template("""
        Musicset:{% for item in array %} <br>
                id: {{ item.id }} <br>
                title: {{ item.set_title }} <br>
                link: {{ item.set_link }} <br>
                tracks: {{ item.set_tracks }} <br>
            {% endfor %}
        """
                               )
    # возвращение шаблона записей
    return result_form.render(array=result)


# роут для вывода, на вход /поле_для_поиска/значение
@app.route('/tracks/<path:val>', methods=['GET', 'POST'])
def tracks_search(val):
    # импортируем модель
    from models import Track
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        # режем поле по '/' первое значение поле, второе значение
        vals_to_search = val.split('/', maxsplit=1)
        # выбор поля по которому будет идти фильтрация, фильтрация + минимальные проверки
        if len(vals_to_search) != 2:
            return 'entered not true value'
        elif vals_to_search[0] == 'id':
            result = Track.query.filter_by(id=vals_to_search[1])
        elif vals_to_search[0] == 'artist':
            result = Track.query.filter_by(artist=vals_to_search[1])
        elif vals_to_search[0] == 'title':
            result = Track.query.filter_by(title=vals_to_search[1])
        elif vals_to_search[0] == 'set_id':
            result = Track.query.filter_by(set_id=vals_to_search[1])
        elif vals_to_search[0]:
            return 'check fields that you entered'
        # шаблон для вывода массива записей
        result_form = Template("""
        Musicset:{% for item in array %} <br>
                id: {{ item.id }} <br>
                track: {{ item.artist }} --
                 {{ item.title }} <br>
                set_id: {{ item.set_id }} <br>
            {% endfor %}
        """
                               )
    # возвращение шаблона записей
    return result_form.render(array=result)


if __name__ == '__main__':
    app.run()
