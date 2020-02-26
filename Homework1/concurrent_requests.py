import concurrent.futures
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import random
import time
import json


latencies = []


def build_all_urls():
    all_urls = []
    base_url = 'http://localhost:9090/concurrent?artist='
    with open('input/artists.txt') as ad:
        artists = ad.readlines()
        for artist in artists:
            artist = artist.strip('\n')
            artist = artist.replace(' ', '+')
            all_urls.append(base_url + artist)
    return all_urls


all_urls = build_all_urls()


def get_random_url():
    random_url = random.choice(all_urls)
    print(random_url)
    return random_url


def single_request(url):
    start_time = time.time()
    session = requests.Session()
    retry = Retry(connect=15, backoff_factor=0.7)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    response = session.get(url)
    latencies.append((time.time() - start_time) * 1000)
    return response.status_code


def write_logs(max_workers, total_requests):
    new_log = dict()
    new_log['total_requests'] = total_requests
    new_log['max_workers'] = max_workers
    new_log['min_latency'] = str(min(latencies)) + ' ms'
    new_log['max_latency'] = str(max(latencies)) + ' ms'
    new_log['avg_latency'] = str(sum(latencies) / len(latencies)) + ' ms'
    with open('logs/concurrent.json') as cdr:
        total_json = json.load(cdr)
        temp = total_json['calls']
        temp.append(new_log)
    with open("logs/concurrent.json", 'w', encoding='utf-8') as cdw:
        json.dump(total_json, cdw, ensure_ascii=False, indent=4)


def lets_do_this(max_workers, total_requests):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_request = {executor.submit(single_request, get_random_url()): _ for _ in range(total_requests)}
        for future in concurrent.futures.as_completed(future_to_request):
            request = future_to_request[future]
            try:
                data = future.result()
                print('%r done with exit_code %r' % (request, data))
            except Exception as exc:
                print('%r generated an exception: %s' % (request, exc))
    write_logs(max_workers, total_requests)


lets_do_this(10, 100)
