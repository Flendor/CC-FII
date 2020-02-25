import json


def init_data():
    with open('input/urls.json') as ud:
        url_file = ud.read()
    with open('input/headers.json') as hd:
        hdr_file = hd.read()
    urls_dict = json.loads(url_file)
    headers_dict = json.loads(hdr_file)
    headers = []
    for elem in headers_dict['api_headers']:
        header_for_one_api = []
        for key, value in elem.items():
            header_for_one_api.append(key)
            header_for_one_api.append(value)
        headers.append(header_for_one_api)
    return urls_dict['api_urls'], urls_dict['extra_urls'], headers
