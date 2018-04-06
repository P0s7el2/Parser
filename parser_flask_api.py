from flask import Flask, jsonify, request, render_template, flash
import config as config
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Track, Musicset


app = Flask(__name__)
app.config.from_object(config)




@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        pass
    if request.method == 'GET':
        pass
    engine = create_engine('sqlite:///test.db')

    Session = sessionmaker(bind=engine)
    session = Session()
    for instance in session.query(Track).order_by(Track.id):
        return instance

        # return jsonify([p.to_dict() for p in set])


if __name__ == '__main__':

    app.run()
