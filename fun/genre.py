import requests
from bs4 import BeautifulSoup
from collections import Counter

def scrape_genre_counts(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    genres = []
    for item in soup.select('.list-group-item'):
        genre_name = item.find('a').text.strip()
        genre_count = int(item.find('span').text.strip())
        genres.append((genre_name, genre_count))

    return genres

def count_genres(genres):
    genre_counter = Counter()
    for genre, count in genres:
        genre_counter[genre] += count
    return genre_counter

if __name__ == "__main__":
    url = "http://127.0.0.1:5000/genres"  # Replace with the actual URL
    genre_data = scrape_genre_counts(url)
    genre_counts = count_genres(genre_data)

    for genre, count in genre_counts.items():
        print(f"{genre}")
