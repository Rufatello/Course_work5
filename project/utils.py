from typing import Any
from googleapiclient.discovery import build
import psycopg2


def get_youtube_data(api_key: str, channel_ids: list[str]) -> list[dict[str, Any]]:
    """Получение данных о каналах и видео с помощью API YouTube."""

    youtube = build('youtube', 'v3', developerKey=api_key)
    data = []
    video_data = []
    next_page_token = None
    # внешний цикл пробегается по id каналу
    for chanel_id in channel_ids:
        # для каждого канала получаем информацию по каналу
        channel_data = youtube.channels().list(part='snippet, statistics', id=chanel_id).execute()
        # во внутреннем цикле получаем информацию по всем видео внутри канала
        while True:
            response = youtube.search().list(part='id,snippet', channelId=chanel_id, type='video',
                                             order='date', maxResults=50, pageToken=next_page_token).execute()
            # сохраняем информацию в список 'video_data'
            video_data.extend(response['items'])
            # переходим к следующему токену
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
        data.append({
            'channel': channel_data['items'][0],
            'videos': video_data
        })
        # a
        return data


def create_database(database_name: str, params: dict) -> None:
    """создание БД и таблиц для сохранения данных о каналах и видео"""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE channels (
                channel_id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                views INTEGER,
                subscribers INTEGER,
                videos INTEGER,
                channel_url TEXT
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE videos (
                video_id SERIAL PRIMARY KEY,
                channel_id INT REFERENCES channels(channel_id),
                title VARCHAR NOT NULL,
                publish_date DATE,
                video_url TEXT
            )
        """)
    conn.commit()
    conn.close()


def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict):
    """Сохранить данные о каналах и видео в БД"""
