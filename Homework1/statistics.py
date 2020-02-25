import json


def form_new_log(url, param, response, latency, status_code):
    new_log = dict()
    new_log['url'] = url + param
    new_log['argument'] = param
    new_log['latency'] = str(latency) + ' ms'
    new_log['status_code'] = status_code
    new_log['response'] = response
    return new_log


def log_deezer(url, param, response, latency, status_code):
    new_log = form_new_log(url, param, response, latency, status_code)
    with open("logs/deezer.json", 'r') as ddr:
        deezer_json = json.load(ddr)
        temp = deezer_json['calls']
        temp.append(new_log)
    with open("logs/deezer.json", 'w', encoding='utf-8') as ddw:
        json.dump(deezer_json, ddw, ensure_ascii=False, indent=4)


def log_random(url, param, response, latency, status_code):
    new_log = form_new_log(url, param, response, latency, status_code)
    with open("logs/random.json", 'r') as rdr:
        random_json = json.load(rdr)
        temp = random_json['calls']
        temp.append(new_log)
    with open("logs/random.json", 'w', encoding='utf-8') as rdw:
        json.dump(random_json, rdw, ensure_ascii=False, indent=4)


def log_songsterr(url, param, response, latency, status_code):
    new_log = form_new_log(url, param, response, latency, status_code)
    with open("logs/songsterr.json", 'r') as sdr:
        songsterr_json = json.load(sdr)
        temp = songsterr_json['calls']
        temp.append(new_log)
    with open("logs/songsterr.json", 'w', encoding='utf-8') as sdw:
        json.dump(songsterr_json, sdw, ensure_ascii=False, indent=4)


def compute_metrics():
    metrics = dict()
    metrics['result'] = "Momentan nu am implementat frate"
    return json.dumps(metrics)
