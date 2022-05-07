import requests
import numpy as np
import requests
# import networkx as nx
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
# from wordcloud import WordCloud
import random

limit = 1000
start = 'https://habr.com/ru/all/'


def get_data(start_link):
	connects = []
	domains = []
	links = []
	page = requests.get(start_link)
	if page.status_code == 200:
		data = page.text
		soup = BeautifulSoup(data, 'lxml')
		links_one_site = []
		for link in soup.find_all('a'):
			links_one_site.append(link.get('href'))
	links_10 = random.sample(links_one_site, 10)
	print(links_10)
	return 0



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
graph(conn)
domain_cloud(dom)
