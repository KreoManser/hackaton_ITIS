# TODO: Разбить на функции (методы или переделать)

import random
from urllib.parse import urljoin, urlparse
# from urllib2 import urlopen
# from urlparse import urljoin
import collections

import requests
import numpy as np
import requests
import networkx as nx
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from wordcloud import WordCloud

limit = 1000
start = 'https://habr.com/ru/all/'

def is_valid(url):
    """
    Проверяет, является ли url допустимым
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


# def bfs(graph, root):
#     visited, queue = set(), collections.deque([root])
#     visited.add(root)
#     while queue:
#         vertex = queue.popleft()
#         for neighbour in graph[vertex]:
#             if neighbour not in visited:
#                 visited.add(neighbour)
#                 queue.append(neighbour)


def get_data(start_link):
    connects = set()
    domains = []
    links = set()
    links_10 = set()
    # connects.add(start_link.split('/')[2])
    page = requests.get(start_link)
    if page.status_code == 200:
        data = page.text
        soup = BeautifulSoup(data, 'lxml')
        links_one_site = []
        for link in soup.find_all('a'):
            href = link.attrs.get("href")
            domains.append(start_link.split('/')[2])
            links_one_site.append(href)
            if any([href == "", href is None, not is_valid(href)]) and (href in links_one_site):
                continue
        while len(links_10) != 10:
            links_10.add(*random.sample(links_one_site, 1))
            # links_10 = random.sample(links_one_site, 10)
        links = links | links_10
        # while len(connects) != 1000:

    print(links_10)
    print(domains)
    print(links)
    return list(connects), domains


def domain_cloud(domains):
    """
    Draw the cloud of words
    Args:
        domains (list of str): ['domain1', 'domain2'...]
    """
    word_string = ' '.join(domains)
    params = dict(background_color="white", width=1200, height=1000, max_words=len(set(domains)))
    wordcloud = WordCloud(**params).generate(word_string)
    plt.imshow(wordcloud)
    plt.show()


def graph(connections, with_labels=True):
    """
    Draw the graph based on a connections
    Args:
        connections (list of tuple): [(A, B), (B, C)...] links from A to B, B to C, etc
        with_labels (bool): plot the labels or not
    """
    g = nx.Graph()
    g.add_edges_from(connections)
    nx.draw(g, verticalalignment='bottom', horizontalalignment='center', with_labels=with_labels, node_size=30)
    plt.show()


conn, dom = get_data(start)
print(conn)
# graph(conn)
# domain_cloud(dom)
