import os
import re
from queue import Queue
from wiki_parse import parse


def build_bridge(path, start_page, end_page):
    if start_page == end_page:
        return [start_page]
    page = start_page
    prev = dict()
    prev[page] = None
    q = Queue()
    q.put(page)
    while page != end_page:
        page = q.get()
        with open(os.path.join(path, page), encoding="utf-8") as file:
            links = re.findall(r"(?<=/wiki/)[\w()]+", file.read())
        for link in links:
            if link == end_page:
                prev[link] = page
                page = end_page
                break
            if os.path.exists(os.path.join(path, link)) and link not in prev:
                prev[link] = page
                q.put(link)

    bridge = []
    while page is not None:
        bridge.append(page)
        page = prev[page]
    bridge.reverse()
    return bridge


def get_statistics(path, start_page, end_page):
    statistics = dict()
    pages = build_bridge(path, start_page, end_page)
    for page in pages:
        statistics[page] = parse(os.path.join(path, page))

    return statistics
