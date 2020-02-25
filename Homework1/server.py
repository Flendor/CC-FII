from http.server import HTTPServer, BaseHTTPRequestHandler
from statistics import compute_metrics
from api_req import RequestController


request_controller = RequestController()


class Server(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path = '/select'

        try:
            if self.path.__contains__('/select'):
                file_to_open = open('index.html').read()
                if self.path.__contains__('artist='):
                    artist = self.path.split('artist=')[1]
                else:
                    artist = None
                if artist is not None:
                    result_1, result_2 = request_controller.request_to_apis(artist)
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
            else:
                raise FileNotFoundError

        except FileNotFoundError:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes('Path not found!', 'utf-8'))


server = HTTPServer(('localhost', 9090), Server)
server.serve_forever()
