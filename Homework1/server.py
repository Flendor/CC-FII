from http.server import HTTPServer, BaseHTTPRequestHandler
from statistics import compute_metrics
from statistics import compute_concurrent_metrics
from api_req import RequestController
from statistics import log_my_server
import time


request_controller = RequestController()


def form_response(file_to_open, artist, concurrent):
    result_1, result_2, final_1, final_2, final_3 = request_controller.request_to_apis(artist, concurrent)
    split_for_result = file_to_open.split('<!-- -->')
    file_to_open = ''
    for index, elem in enumerate(split_for_result):
        file_to_open += elem
        if index == 0:
            file_to_open += "<h3> Results for the last call: </h3>"
        if index == 1:
            file_to_open += result_1
        if index == 2:
            break
    if result_2 is not None:
        file_to_open += "Learn the song <a href=" + result_2 + ">HERE</a>" + split_for_result[3]
    else:
        file_to_open += "Sorry, we couldn't find a guitar tab for that song!" + split_for_result[3]
    return file_to_open, final_1, final_2, final_3


class Server(BaseHTTPRequestHandler):

    def do_GET(self):
        start_time = time.time()
        if self.path == '/':
            self.path = '/select'

        try:
            if self.path.__contains__('/select'):
                file_to_open = open('index.html').read()
                if self.path.__contains__('artist='):
                    artist = self.path.split('artist=')[1]
                else:
                    artist = None
                if artist is not None and len(artist) > 0:
                    file_to_open, final_1, final_2, final_3 = form_response(file_to_open, artist, False)
                    final_time = (time.time() - start_time) * 1000
                    log_my_server(self.path, artist, file_to_open, final_time, 200, final_1, final_2, final_3)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(file_to_open, 'utf-8'))
            elif self.path.endswith('/metrics'):
                metrics = compute_metrics()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(bytes(metrics, 'utf-8'))
            elif self.path.__contains__('/concurrent'):
                file_to_open = open('index.html').read()
                if self.path.__contains__('artist='):
                    artist = self.path.split('artist=')[1]
                else:
                    artist = None
                file_to_open, final_1, final_2, final_3 = form_response(file_to_open, artist, True)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(file_to_open, 'utf-8'))
            elif self.path.endswith('/conmetrics'):
                conmetrics = compute_concurrent_metrics()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(bytes(conmetrics, 'utf-8'))
            else:
                raise FileNotFoundError

        except FileNotFoundError:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes('Path not found!', 'utf-8'))

        except Exception as e:
            print(e)


server = HTTPServer(('localhost', 9090), Server)
server.serve_forever()
