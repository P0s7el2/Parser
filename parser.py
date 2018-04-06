import requests
import asyncio
from bs4 import BeautifulSoup
from time import time
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column, Integer, String
from models import Track, Musicset
from sqlalchemy.orm import sessionmaker

import aiohttp

domain = 'http://zaycev.net'


def start_db():
    # устанавливаем соединение с бд
    engine = create_engine('sqlite:///test.db')
    # инициализируем сесисю
    Session = sessionmaker(bind=engine)
    session = Session()
    # создаем таблицу
    metadata = MetaData()
    # удаляем данные из таблиц
    Track.__table__.drop(engine)
    Musicset.__table__.drop(engine)
    tracks_table = Table('tracks', metadata,
                         Column('id', Integer, primary_key=True),
                         Column('artist', String),
                         Column('title', String),
                         Column('set_id', String)
                         )
    misicsets_table = Table('musicsets', metadata,
                            Column('id', Integer, primary_key=True),
                            Column('set_title', String),
                            Column('set_link', String),
                            Column('set_tracks', String)
                            )
    metadata.create_all(engine)
    # определяем новый класс, от которого будет унаслед ORM-класс
    return session


async def get_html(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()


def get_all_links(html):
    """
   Return links for musicsets
   :param html: str, html code of page
   :return: array of links
   """
    # парсим код
    soup = BeautifulSoup(html, 'lxml')
    # ищем элемент который содержит сборки, потом ищем эл со сборками и вставляем, ограничиваем количество 10ю
    lis = soup.find('ul', class_='musicset-list unstyled-list clearfix') \
        .findAll('li', class_='musicset-list__item ', limit=20)

    links = {}
    # проходимся по эл сборки и находим там ссылку на страницу сборки и название,
    # вставляем в массив
    i = 0
    for li in lis:
        i += 1
        a = li.find('a').get('href')
        title = li.find('img').get('alt').replace('Музыкальная подборка: ', '')
        # вероятно надо было бы формировать словарь в виде {[id: 1], [url:a.com], [title:kek]}
        links[i] = [a, title]
    return links


async def parse_links(musicsets):
    # Перебор словарая
    tracks = [get_musicset(musicsets[id][0], id) for id in musicsets]
    completed, pending = await asyncio.wait(tracks)
    result = []
    for item in completed:
        result.append(item.result())
    return result


async def get_musicset(url, id):
    # получаем html страницы со сборкой

    html = await get_html(domain + url)
    # парсим html страницы со сборкой
    soup = BeautifulSoup(html, 'lxml')
    # находим элемент с инфой о сборке
    main_block = soup.find('div', class_='block musicset clearfix')
    # находим русское название сборки (для будующего функционала)
    set_title = main_block.find('h1', class_='block__header musicset__title')
    # находим все блоки с песнями
    tracks_block = main_block.findAll('div', class_='musicset-track__title track-geo__title')
    # иниц массив с назавниями треков
    tracks = {}
    # проходимся по элементам с названиями, находим название и пихаем в ф-ию отправления в бд и в массив
    for track in tracks_block:
        track_artist = track.find('div', class_='musicset-track__artist').get_text()
        track_title = track.find('div', class_='musicset-track__track-name').get_text()
        tracks[track_artist, track_title] = id
    return tracks


def set_tracks_to_db(tracks, session):
    # добавляем трек
    for track in tracks:
        artist = track[0]
        title = track[1]
        set_id = tracks.get(track, -1)
        session.add(Track(artist, title, set_id))

    # комитим
    session.commit()


def set_musicsets_to_db(id, musicset, set_tracks, session):
    set_link = musicset[0]
    set_title = musicset[1]
    session.add(Musicset(id, set_tracks, set_link, set_title))
    session.commit()


def get_all_sets(url):
    res = requests.get(url)
    return res.text


def main():
    tic = time()
    global domain
    # получаем все ссылки на сборки
    musicsets = get_all_links(get_all_sets(domain + '/musicset/'))
    # открываем ссесию
    session = start_db()
    event_loop = asyncio.get_event_loop()
    try:
        # получаем песни
        results = event_loop.run_until_complete(parse_links(musicsets))
    finally:
        event_loop.close()

    for array_of_set_tracks in results:
        set_tracks_to_db(array_of_set_tracks, session)
    for cur_set_id in musicsets:
        set_tracks = ''
        for row in session.query(Track).filter_by(set_id=cur_set_id).all():
            set_tracks += str(row.id)+', '
        set_musicsets_to_db(cur_set_id, musicsets[cur_set_id], set_tracks, session)
    toc = time()

    print(toc - tic)


if __name__ == '__main__':
    main()
