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
    track_session = db.session.query(Track)
    if search:
        if select == 'artist':
            result = Track.query.filter(Track.artist.ilike('%{0}%'.format(search)))
        elif select == 'track_title':
            result = Track.query.filter(Track.title.ilike('%{0}%'.format(search)))
        elif select == 'set_title':
            mst = Musicset.query.filter(Musicset.set_title.ilike('%{0}%'.format(search)))
            result = []
            for item in mst:
                id = str(item.id)
                result.extend(Track.query.filter_by(set_id=id))
        elif select == '-':
            d = track_session.filter(Track.artist.ilike('%{0}%'.format(search)) | Track.title.ilike('%{0}%'.format(search)))
            d.delete(synchronize_session=False)
            db.session.commit()
            result = Track.query.all()
        elif select == 'plus':
            d = track_session.filter(Track.artist.ilike('%{0}%'.format(search)) | Track.title.ilike('%{0}%'.format(search)))
            track_session.delete()
            db.session.add_all(d)
            db.session.commit()
            result = d
    else:
        # достаем ве записи
        result = Track.query.all()

    # возвращаем темплейт чтобы вывести заиси
    return render_template('start.html', mst=result)


if __name__ == '__main__':
    app.run()
