import requests
from bs4 import BeautifulSoup

url = 'http://127.0.0.1:5000/hanime/shocking-pink'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

"""episodes = soup.find_all('li', class_='list-group-item')

episode_links = []
for episode in episodes[1:]:  # Skip the first item as it is the header
    link = episode.find('a')['href']
    episode_links.append(link)

print(episode_links)
"""
links = []
for item in soup.select('.list-group-item a'):
    links.append(item['href'])

print(links)
