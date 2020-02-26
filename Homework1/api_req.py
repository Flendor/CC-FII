from initializer import init_data
import requests
import time
from statistics import log_deezer, log_random, log_songsterr


def request_to_deezer(artist, url, header_name, header_value, concurrent):
    start_time = time.time()
    try:
        songs = requests.get(url + artist, headers={header_name: header_value})
        final_time = (time.time() - start_time) * 1000
        songs_json = songs.json()
        return songs_json, final_time
    except requests.exceptions.RequestException as e:
        final_time = (time.time() - start_time) * 1000
        songs_json = "Request Failed"
        print("Deezer request failed!")
        print(e)
    finally:
        print("deezer succeeded")
        if not concurrent:
            log_deezer(url, artist, songs_json, final_time, songs.status_code)


def request_to_random(url, artist, header_name, header_value, concurrent):
    start_time = time.time()
    try:
        love = requests.get(url + artist, headers={header_name: header_value})
        final_time = (time.time() - start_time) * 1000
        love_json = love.json()
        return love_json, final_time
    except requests.exceptions.RequestException as e:
        final_time = (time.time() - start_time) * 1000
        love_json = "Request Failed"
        print("LoveCalculator request failed!")
        print(e)
    finally:
        print("random succeeded")
        if not concurrent:
            log_random(url, artist, love_json, final_time, love.status_code)


def request_to_songsterr(url, song_title, concurrent):
    start_time = time.time()
    try:
        songs_from_songsterr = requests.get(url + song_title)
        final_time = (time.time() - start_time) * 1000
        songs_from_songsterr_json = songs_from_songsterr.json()
        return songs_from_songsterr_json, final_time
    except requests.exceptions.RequestException as e:
        final_time = (time.time() - start_time) * 1000
        songs_from_songsterr_json = "Request Failed"
        print("Songsterr request failed!")
        print(e)
    finally:
        print("songsterr succeeded")
        if not concurrent:
            log_songsterr(url, song_title, songs_from_songsterr_json, final_time, songs_from_songsterr.status_code)


class RequestController:

    def __init__(self):
        self.data = init_data()

    def request_to_apis(self, artist, concurrent):
        try:
            songs_json, final_deezer_time = request_to_deezer(artist, self.data[0][0], self.data[2][0][0], self.data[2][0][1], concurrent)
            love_json, final_random_time = request_to_random(self.data[0][1], artist,
                                            self.data[2][1][0], self.data[2][1][1], concurrent)
            percentage = int(love_json['percentage'])
            if percentage == 0:
                percentage += 1
            print(len(songs_json['data']))
            song_index = percentage % len(songs_json['data'])
            result_1 = "We chose song number " + str(song_index) + \
                       " (" + songs_json['data'][song_index]['title_short'] + \
                       ") by <b>" + artist.upper().replace('+', ' ') + "</b> because you love " + \
                       'this artist ' + ' ' + love_json['percentage'] + '%!'
            songsterr_json, final_songsterr_time = request_to_songsterr(self.data[0][2], songs_json['data'][song_index]['title_short'], concurrent)
            tab_id = None
            for elem in songsterr_json:
                if elem['artist']['name'].lower() == artist.lower().replace('+', ' ') and \
                        elem['title'].lower() == songs_json['data'][song_index]['title_short'].lower():
                    tab_id = elem['id']
            if tab_id is None:
                result_2 = None
            else:
                result_2 = self.data[1][0] + str(tab_id)
            return result_1, result_2, final_deezer_time, final_random_time, final_songsterr_time
        except Exception as e:
            print("Requests failed")
            print(e)
