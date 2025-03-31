import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import os
import re

def get_url():
    """Get page url"""
    baseUrl = 'https://hdtodayz.to/movie?page='
    return baseUrl
def clean_filename(title):
    """Remove invalid characters from filenames"""
    return re.sub(r'[\\/*?:"<>|]', '_', title)
def download_image(image_url, title):
    try:
        parsed_url = urlparse(image_url)
        response = requests.get(image_url, stream=True)
        extension = os.path.splitext(parsed_url.path)[-1] if os.path.splitext(parsed_url.path)[-1] else ".jpg"
        filename = f"{title}{extension}"
        save_dir = os.path.join(os.getcwd(), 'movie_posters')

        filepath = os.path.join(save_dir, filename)
        if response.status_code == 200:
            #ensure the dir exists
            # Clean filename
            filename = f"{clean_filename(title)}{extension}"
            os.makedirs(save_dir, exist_ok=True)
            #save the image file
            with open(filepath, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print('succesfully downloaded', filename)
        else:
            print('an error occurred')
    except Exception as e:
        print("\nAn error occured downloading image\n", e)
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

            # Extract image URL safely
            image_tag = movie.find('img', class_="film-poster-img")
            if image_tag:
                image_url = image_tag.get('data-src') or image_tag.get('src', None)
                if image_url:
                    full_image_url = urljoin(baseUrl, image_url)

                    # Clean title for filename
                    image_title = title.replace(' ', '_').replace('/', '_')
                    print(image_title)
                    download_image(full_image_url, image_title)
                else:
                    print("Error occured fetching image")
          
            # urls = [link.get_attribute("href") for link in links if link.get_attribute("href")]
            fd_info = movie.find('div', class_='fd-infor')
            release_date = movie.find('span', class_= 'fdi-item').get_text(strip=True)
            
            print('film-name:', title, ' release-date:', release_date) 
        # print( 'link: ', image_url)
        
    except requests.RequestException as e:
        print("Error fetching the page")

if __name__ == '__main__':
    baseUrl = get_url()
    for page in range(1,3):
        scrape_movie(baseUrl, page)