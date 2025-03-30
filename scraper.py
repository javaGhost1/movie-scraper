import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse
import os

def get_url():
    """Get page url"""
    baseUrl = 'https://hdtodayz.to/movie?page='
    return baseUrl

def download_image(image_url, title):
    try:
        parsed_url = urlparse(image_url)
        response = requests.get(image_url, stream=True)
        extension = os.path.splitext(image_url)[-1] or ".jpg"
        filename = f"{title}{extension}"
        if response.status_code == 200:
            #ensure the dir exists
            save_dir = os.path.join(os.getcwd(), 'movie_posters')
            os.makedirs(save_dir, exist_ok=True)
            #save the image file
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print('succesfully downloaded', filename)
        else:
            print('an error occurred')
    except Exception as e:
        print("An error occure downloading image")
        return None
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
            link = movie.find('a', class_="film-poster-ahref flw-item-tip")
            title = movie.find('h2', class_='film-name').text.strip()

            image_tag = movie.find('img', class_="film-poster-img lazyloaded" )
            image_url = image_tag['data-src'] if image_tag and 'data-src' in image_tag.attrs else image_tag.get('src', '')

            image_url = image_tag['data-src'] if image_tag and 'data-src' in image_tag.attrs else image_tag.get('src', '')
            image_title = title.replace(' ', '_').replace('/', '_')

            if image_url:
                full_image_url = urljoin(baseUrl, image_url)
                download_image(full_image_url, image_title)
            # urls = [link.get_attribute("href") for link in links if link.get_attribute("href")]
            fd_info = movie.find('div', class_='fd-infor')
            release_date = movie.find('span', class_= 'fdi-item').get_text(strip=True)
            print(f"🎬 {title} | 📅 {release_date}")
        # print('film-name:', title, ' release-date:', release_date) 
        # print( 'link: ', image_url)
        
    except requests.RequestException as e:
        print("Error fetching the page")

if __name__ == '__main__':
    baseUrl = get_url()
    for page in range(1,50):
        scrape_movie(baseUrl, page)