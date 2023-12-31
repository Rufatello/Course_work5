"""основная логика программы в файле main.py здесь испорты функций """
import os
from config import config
from utils import get_youtube_data, create_database, save_data_to_database


def main():
    api_key = os.getenv('You-Tube-API')
    # данные об ид каналах которые будем получать
    channel_ids = [
        'UC-OVMPlMA3-YCIeg4z5z23A',  # moscowpython
        # 'UCwHL6WHUarjGfUM_586me8w',  # highload

    ]
    params = config()
    data = get_youtube_data(api_key, channel_ids)
    create_database('youtube', params)
    # save_data_to_database(data, 'youtube', params)


if __name__ == '__main__':
    main()
