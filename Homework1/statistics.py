import json
import re


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


def log_my_server(url, param, response, latency, status_code, latency_1, latency_2, latency_3):
    new_log = form_new_log(url, param, response, latency, status_code)
    new_log['url'] = url
    new_log['deezer_latency'] = str(latency_1) + ' ms'
    new_log['random_latency'] = str(latency_2) + ' ms'
    new_log['songsterr_latency'] = str(latency_3) + ' ms'
    with open("logs/total.json", 'r') as tdr:
        total_json = json.load(tdr)
        temp = total_json['calls']
        temp.append(new_log)
    with open("logs/total.json", 'w', encoding='utf-8') as tdw:
        json.dump(total_json, tdw, ensure_ascii=False, indent=4)


def compute_metrics():
    metrics = dict()
    with open('logs/total.json', 'r') as td:
        server_logs = json.loads(td.read())
    server_latencies = []
    deezer_latencies = []
    random_latencies = []
    songsterr_latencies = []
    if len(server_logs['calls']) > 0:
        for elem in server_logs['calls']:
            server_latencies.append(elem['latency'])
            deezer_latencies.append(elem['deezer_latency'])
            random_latencies.append(elem['random_latency'])
            songsterr_latencies.append(elem['songsterr_latency'])
        pattern = re.compile('\s*ms')
        server_latencies = list(map(lambda x: float(re.sub(pattern, '', x)), server_latencies))
        deezer_latencies = list(map(lambda x: float(re.sub(pattern, '', x)), deezer_latencies))
        random_latencies = list(map(lambda x: float(re.sub(pattern, '', x)), random_latencies))
        songsterr_latencies = list(map(lambda x: float(re.sub(pattern, '', x)), songsterr_latencies))
        metrics.update({'my_server': {'max_latency': str(max(server_latencies)) + ' ms',
                                      'min_latency': str(min(server_latencies)) + ' ms',
                                      'avg_latency': str(sum(server_latencies) / len(server_latencies)) + ' ms'}})
        metrics.update({'deezer': {'max_latency': str(max(deezer_latencies)) + ' ms',
                                   'min_latency': str(min(deezer_latencies)) + ' ms',
                                   'avg_latency': str(sum(deezer_latencies) / len(deezer_latencies)) + ' ms'}})
        metrics.update({'random': {'max_latency': str(max(random_latencies)) + ' ms',
                                   'min_latency': str(min(random_latencies)) + ' ms',
                                   'avg_latency': str(sum(random_latencies) / len(random_latencies)) + ' ms'}})
        metrics.update({'songsterr': {'max_latency': str(max(songsterr_latencies)) + ' ms',
                                      'min_latency': str(min(songsterr_latencies)) + ' ms',
                                      'avg_latency': str(sum(songsterr_latencies) / len(songsterr_latencies)) + ' ms'}})
        metrics['all_requests'] = server_logs

    else:
        metrics['response'] = "Sorry, there is no data in the logs!"
    return json.dumps(metrics)


def compute_concurrent_metrics():
    with open('logs/concurrent.json', 'r') as cd:
        concurrent_logs = json.loads(cd.read())
    return json.dumps(concurrent_logs)
