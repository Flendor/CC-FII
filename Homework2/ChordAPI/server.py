from http.server import HTTPServer, BaseHTTPRequestHandler
from operations import get_chord_name_from_url, get_name_from_url, is_chord_body_valid, \
    is_song_body_valid, get_sid_from_url
from db_helper import get_single_chord_response, get_songs_by_artist, get_song_by_name, \
    get_song_by_id, insert_chord_into_db, insert_song_into_db, update_chord_in_db, update_song_in_db, \
    delete_chord_from_db, delete_song_from_db
import sqlite3
import json


conn = sqlite3.connect("chord.db")


class Server(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.__contains__('/chord/'):
            chord_name = get_chord_name_from_url(self.path)
            try:
                response = get_single_chord_response(conn, chord_name)
                self.send_response(response[1])
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(bytes(json.dumps(response[0]), 'utf-8'))
            except Exception as e:
                print(e)
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"Response": "There was a problem with the database."}
                self.wfile.write(bytes(json.dumps(response), 'utf-8'))

        elif self.path.__contains__('/song/artist/'):
            artist_name = get_name_from_url(self.path)
            try:
                response = get_songs_by_artist(conn, artist_name)
                self.send_response(response[1])
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(bytes(json.dumps(response[0]), 'utf-8'))
            except Exception as e:
                print(e)
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"Response": "There was a problem with the database."}
                self.wfile.write(bytes(json.dumps(response), 'utf-8'))

        elif self.path.__contains__('/song/name/'):
            song_name = get_name_from_url(self.path)
            try:
                response = get_song_by_name(conn, song_name)
                self.send_response(response[1])
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(bytes(json.dumps(response[0]), 'utf-8'))
            except Exception as e:
                print(e)
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"Response": "There was a problem with the database."}
                self.wfile.write(bytes(json.dumps(response), 'utf-8'))

        elif self.path.__contains__('/song/id/'):
            try:
                song_id = get_sid_from_url(self.path)
                response = get_song_by_id(conn, song_id)
                self.send_response(response[1])
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(bytes(json.dumps(response[0]), 'utf-8'))
            except Exception as e:
                print(e)
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"Response": "There was a problem with the database."}
                self.wfile.write(bytes(json.dumps(response), 'utf-8'))

        else:
            response = {"Response": "Bad url"}
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

    def do_POST(self):
        if self.path.__contains__('/chord'):
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            if is_chord_body_valid(json.loads(body.decode('utf-8'))):
                try:
                    response = insert_chord_into_db(conn, json.loads(body.decode('utf-8')))
                    self.send_response(response[1])
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(bytes(json.dumps(response[0]), 'utf-8'))
                except Exception as e:
                    print(e)
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {"Response": "There was a problem with the database."}
                    self.wfile.write(bytes(json.dumps(response), 'utf-8'))
            else:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response_dict = dict()
                response_dict['Response'] = 'Body is not valid!'
                self.wfile.write(bytes(json.dumps(response_dict), 'utf-8'))

        elif self.path.__contains__('/song'):
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            if is_song_body_valid(json.loads(body.decode('utf-8'))):
                try:
                    response = insert_song_into_db(conn, json.loads(body.decode('utf-8')))
                    self.send_response(response[1])
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(bytes(json.dumps(response[0]), 'utf-8'))
                except Exception as e:
                    print(e)
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {"Response": "There was a problem with the database."}
                    self.wfile.write(bytes(json.dumps(response), 'utf-8'))
            else:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response_dict = dict()
                response_dict['Response'] = 'Body is not valid!'
                self.wfile.write(bytes(json.dumps(response_dict), 'utf-8'))
        else:
            response = {"Response": "Bad url"}
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

    def do_PUT(self):
        if self.path.__contains__('/chord/'):
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            if is_chord_body_valid(json.loads(body.decode('utf-8'))):
                try:
                    chord_name = get_chord_name_from_url(self.path)
                    response = update_chord_in_db(conn, json.loads(body.decode('utf-8')), chord_name)
                    self.send_response(response[1])
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(bytes(json.dumps(response[0]), 'utf-8'))
                except Exception as e:
                    print(e)
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {"Response": "There was a problem with the database."}
                    self.wfile.write(bytes(json.dumps(response), 'utf-8'))
            else:
                self.send_response(405)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response_dict = dict()
                response_dict['Response'] = 'Body is not valid or complete!'
                self.wfile.write(bytes(json.dumps(response_dict), 'utf-8'))

        elif self.path.__contains__('/song/id/'):
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            if is_song_body_valid(json.loads(body.decode('utf-8'))):
                try:
                    song_id = get_sid_from_url(self.path)
                    response = update_song_in_db(conn, json.loads(body.decode('utf-8')), song_id)
                    self.send_response(response[1])
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(bytes(json.dumps(response[0]), 'utf-8'))
                except Exception as e:
                    print(e)
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {"Response": "There was a problem with the database."}
                    self.wfile.write(bytes(json.dumps(response), 'utf-8'))
            else:
                self.send_response(405)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response_dict = dict()
                response_dict['Response'] = 'Body is not valid!'
                self.wfile.write(bytes(json.dumps(response_dict), 'utf-8'))
        else:
            response = {"Response": "Bad url"}
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

    def do_DELETE(self):
        if self.path.__contains__('/chord/'):
            chord_name = get_chord_name_from_url(self.path)
            try:
                response = delete_chord_from_db(conn, chord_name)
                self.send_response(response[1])
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(bytes(json.dumps(response[0]), 'utf-8'))
            except Exception as e:
                print(e)
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"Response": "There was a problem with the database."}
                self.wfile.write(bytes(json.dumps(response), 'utf-8'))

        elif self.path.__contains__('/song/id/'):
            song_id = get_sid_from_url(self.path)
            try:
                response = delete_song_from_db(conn, song_id)
                self.send_response(response[1])
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(bytes(json.dumps(response[0]), 'utf-8'))
            except Exception as e:
                print(e)
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"Response": "There was a problem with the database."}
                self.wfile.write(bytes(json.dumps(response), 'utf-8'))
        else:
            response = {"Response": "Bad url"}
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(response), 'utf-8'))


server = HTTPServer(('localhost', 9090), Server)
server.serve_forever()
