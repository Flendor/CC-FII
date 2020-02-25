from initializer import init_data
import requests
import time
from statistics import log_deezer, log_random, log_songsterr


def request_to_deezer(artist, url, header_name, header_value):
    start_time = time.time()
    try:
        songs = requests.get(url + artist, headers={header_name: header_value})
        songs_json = songs.json()
        return songs_json
    except Exception as e:
        songs_json = "Request Failed"
        print("Deezer request failed!")
        print(e)
    finally:
        final_time = (time.time() - start_time) * 1000
        log_deezer(url, artist, songs_json, final_time, songs.status_code)


def request_to_random(url, max_random_value, header_name, header_value):
    start_time = time.time()
    try:
        number = requests.get(url + max_random_value, headers={header_name: header_value})
        number_json = number.json()
        return number_json
    except Exception as e:
        number_json = "Request Failed"
        print("NumbersApi request failed!")
        print(e)
    finally:
        final_time = (time.time() - start_time) * 1000
        log_random(url, max_random_value, number_json, final_time, number.status_code)


def request_to_songsterr(url, song_title):
    start_time = time.time()
    try:
        songs_from_songsterr = requests.get(url + song_title)
        songs_from_songsterr_json = songs_from_songsterr.json()
        return songs_from_songsterr_json
    except Exception as e:
        songs_from_songsterr_json = "Request Failed"
        print("Songsterr request failed!")
        print(e)
    finally:
        final_time = (time.time() - start_time) * 1000
        log_songsterr(url, song_title, songs_from_songsterr_json, final_time, songs_from_songsterr.status_code)


class RequestController:

    def __init__(self):
        self.data = init_data()

    def request_to_apis(self, artist):
        try:
            songs_json = request_to_deezer(artist, self.data[0][0], self.data[2][0][0], self.data[2][0][1])
            number_json = request_to_random(self.data[0][1], str(len(songs_json['data']) - 1),
                                            self.data[2][1][0], self.data[2][1][1])
            song_index = number_json['number']
            result_1 = "We chose song number " + str(song_index) + \
                       " (" + songs_json['data'][song_index]['title_short'] + \
                       ") by <b>" + artist.upper().replace('+', ' ') + "</b> because " + number_json['text']
            songsterr_json = request_to_songsterr(self.data[0][2], songs_json['data'][song_index]['title_short'])
            tab_id = None
            for elem in songsterr_json:
                if elem['artist']['name'].lower() == artist.lower() and \
                        elem['title'] == songs_json['data'][song_index]['title_short']:
                    tab_id = elem['id']
            if tab_id is None:
                result_2 = None
            else:
                result_2 = self.data[1][0] + str(tab_id)
            return result_1, result_2
        except Exception as e:
            print("Requests failed")
            print(e)
