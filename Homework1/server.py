import cgi
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler


artist = None


def read_urls():
    urls = []
    keys = []
    with open("urls.txt") as fd:
        lines = fd.readlines()
        for line in lines:
            line = line.strip('\n')
            urls.append(line)
    with open("headers.txt") as fd:
        lines = fd.readlines()
        for line in lines:
            line = line.strip('\n')
            keys.append(line)
    return urls, keys


data = read_urls()


def request_to_api():
    try:
        if artist is not None:
            songs = requests.get(data[0][0] + artist, headers={data[1][0]: data[1][1]})
            songs_json = songs.json()
            number = requests.get(data[0][1] + str(len(songs_json['data']) - 1), headers={data[1][2]: data[1][3]})
            number_json = number.json()
            song_index = number_json['number']
            result_1 = "We chose song number " + str(song_index) + \
                     " (" + songs_json['data'][song_index]['title_short'] + ") because " + number_json['text']
            songs_from_songsterr = requests.get(data[0][2] + songs_json['data'][song_index]['title_short'])
            songs_from_songsterr_json = songs_from_songsterr.json()
            tab_id = None
            for elem in songs_from_songsterr_json:
                if elem['artist']['name'].lower() == artist.lower():
                    tab_id = elem['id']
            if tab_id is None:
                result_2 = "Sorry, we could not find a tab for the song!"
            else:
                result_2 = data[0][3] + str(tab_id)
            return result_1, result_2
    except:
        print("Requests failed")


class Server(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path = '/select'

        try:
            if self.path.endswith('/select'):
                file_to_open = open('index.html').read()
            elif self.path.endswith('/result'):
                if artist is not None:
                    print(artist)
                    result_1, result_2 = request_to_api()
                    file_to_open = "<html> <body> </body> <p>" + result_1 + \
                                   "</p> <p> You must learn this song now: <a href=" + result_2 + \
                                   ">Click here </a> </p> </html>"
            self.send_response(200)

        except FileNotFoundError:
            file_to_open = 'File not found!'
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))



    def do_POST(self):
        if self.path.endswith('/result'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            if ctype == 'multipart/form-data':
                pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
                content_len = int(self.headers.get('Content-Length'))
                pdict['CONTENT-LENGTH'] = content_len
                fields = cgi.parse_multipart(self.rfile, pdict)
                global artist
                artist = fields.get('artist')[0]
        self.send_response(301)
        self.send_header('content-type', 'text/html')
        self.send_header('Location', '/result')
        self.end_headers()


server = HTTPServer(('localhost', 9000), Server)
server.serve_forever()
