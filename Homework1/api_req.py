from initializer import init_data
import requests


def request_to_deezer(artist, url, header_name, header_value):
    try:
        songs = requests.get(url + artist, headers={header_name: header_value})
        songs_json = songs.json()
        return songs_json
    except:
        print("Deezer request failed!")


def request_to_random(url, max_random_value, header_name, header_value):
    try:
        number = requests.get(url + max_random_value, headers={header_name: header_value})
        number_json = number.json()
        return number_json
    except:
        print("NumbersApi request failed!")
    finally:



def request_to_songsterr(url, song_title):
    try:
        songs_from_songsterr = requests.get(url + song_title)
        songs_from_songsterr_json = songs_from_songsterr.json()
        return songs_from_songsterr_json
    except:
        print("Songsterr request failed!")


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
                if elem['artist']['name'].lower() == artist.lower():
                    tab_id = elem['id']
            if tab_id is None:
                result_2 = None
            else:
                result_2 = self.data[1][0] + str(tab_id)
            return result_1, result_2
        except:
            print("Requests failed")
