import requests
import numpy as np
import requests
import networkx as nx
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from wordcloud import WordCloud

limit = 1000
start = '????'

def get_data(start_link):
	connects = []
	domains = []
	link = "https://habr.com/ru/all/"
	page = requests.get(link)
	if page.status_code == 200:
		print(page.text)
	soup = BeautifulSoup(page, 'lxml')

	for product in soup.findAll('a', attrs={'href': 'item'}):  # берем блок див по аттрибутам
		title = product.findChildren('h3', attrs={'itemprop': 'name'})[0].text  # берем название товара
		# (из списка первый элемент в текст)
		link = product.findChildren('a', attrs={'data-marker': 'item-title'})[0]  # поиск ссылки по атрибуту
		link = "https://www.avito.ru" + link.get('href', None)
		# print(link)
		''' Это класс! '''
		price = product.findChildren('meta', attrs={'itemprop': 'price'})[0]
		price = int(price.get('content', 0))
		print(f"{title}, цена: {price}, ссылка: {link}")

	return connects, domains


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
