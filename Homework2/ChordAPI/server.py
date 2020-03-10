from http.server import HTTPServer, BaseHTTPRequestHandler
from operations import get_chord_name_from_url, get_name_from_url
from db_helper import get_single_chord_response, get_songs_by_artist, get_song_by_name
import sqlite3
import json


conn = sqlite3.connect("chord.db")


class Server(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.__contains__('/chord/'):
            chord_name = get_chord_name_from_url(self.path)
            response = get_single_chord_response(conn, chord_name)
            self.send_response(response[1])
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(response[0]), 'utf-8'))

        elif self.path.__contains__('/song/artist/'):
            artist_name = get_name_from_url(self.path)
            response = get_songs_by_artist(conn, artist_name)
            self.send_response(response[1])
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(response[0]), 'utf-8'))

        elif self.path.__contains__('/song/name/'):
            song_name = get_name_from_url(self.path)
            response = get_song_by_name(conn, song_name)
            self.send_response(response[1])
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(response[0]), 'utf-8'))

        else:
            response = {"Response": "Bad request"}
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(response), 'utf-8'))


server = HTTPServer(('localhost', 9090), Server)
server.serve_forever()
