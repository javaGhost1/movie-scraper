import requests
from bs4 import BeautifulSoup
import os

def get_url():
    """Get page url"""
    baseUrl = 'https://hdtodayz.to/movie?page='
    # baseUrl = 'https://ww19.0123movie.net/list/movies/page/2.html'
    return baseUrl

def scrape_movie(baseUrl, page):
    """Scrape for movies"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.163 Mobile Safari/537.36'
    }
    try:
        res = requests.get(baseUrl+str(page), headers=headers)
        res.raise_for_status()
        movies = []
        soup = BeautifulSoup(res.content, 'html.parser')
        movie_listing = soup.find_all('div', class_='flw-item')
        for movie in movie_listing:
            title = movie.find('h2', class_='film-name').text.strip()
            fd_info = movie.find('div', class_='fd-infor')
            if fd_info:
                release_date = movie.find('span', class_= 'fdi-item').get_text(strip=True)
        print('film-name:', title, ' release-date:', release_date) 
        
    except requests.RequestException as e:
        print("Error fetching the page")

if __name__ == '__main__':
    baseUrl = get_url()
    for page in range(1,50):
        scrape_movie(baseUrl, page)