from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

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
    # получаем то что у нас в select и search
    search = request.args.get('search')
    select = request.args.get('select')
    # создаем сессию / подключение к можели Track
    track_session = db.session.query(Track)
    # если существует переменная search
    if search:
        # если выбран артист
        if select == 'artist':
            # фильтруем артиста по введенному значению, возвращаем треки
            result = track_session.filter(Track.artist.ilike('%{0}%'.format(search)))
        # если выбрано название трека
        elif select == 'track_title':
            # фильтруем треки по введенному названию, возвращаем треки
            result = track_session.filter(Track.title.ilike('%{0}%'.format(search)))
        # если выбрано название сборки
        elif select == 'set_title':
            # фильтруем по названию сборки, возвращаем сборки
            mst = Musicset.query.filter(Musicset.set_title.ilike('%{0}%'.format(search)))
            # инициализируем массив для треков
            result = []
            # проходим по выбранным сборкам
            for item in mst:
                # приводим id борки в str
                id = str(item.id)
                # фильтруем нужные нам треки и добавляем их в массив
                result.extend(Track.query.filter_by(set_id=id))
        # если выбран minus
        elif select == 'minus':
            # фильтруем треки по артисту и названию
            d = track_session.filter(Track.artist.ilike('%{0}%'.format(search)) | Track.title.ilike('%{0}%'.format(search)))
            # удаляем найденные
            d.delete(synchronize_session=False)
            # комитим
            db.session.commit()
            # возвращаем оставшиеся треки
            result = Track.query.all()
        # если выбран plus
        elif select == 'plus':
            # если искомое значение не найдено в поле артиста или названия трека, то удаляем трек
            track_session.filter(~(Track.artist.ilike('%{0}%'.format(search))
                                   | Track.title.ilike('%{0}%'.format(search))
                                   ))\
                .delete(synchronize_session=False)
            # комитим
            db.session.commit()
            # возвращаем оставшиеся треки
            result = Track.query.all()
    #  если переменная не существует
    else:
        # достаем ве записи
        result = Track.query.all()

    # возвращаем темплейт чтобы вывести заиси
    return render_template('start.html', mst=result)


if __name__ == '__main__':
    app.run()
