import requests
from django.shortcuts import render
from .forms import MovieSearchForm
from bs4 import BeautifulSoup

def search_movie(request):
    form = MovieSearchForm()
    movie_data = None
    download_link = None

    if request.method == 'POST':
        form = MovieSearchForm(request.POST)
        if form.is_valid():
            movie_name = form.cleaned_data['movie_name']
            try:
                print(f"Fetching data for movie: {movie_name}")
                response = requests.get(f'http://www.omdbapi.com/?i=tt3896198&apikey=2a9b32e4={movie_name}', timeout=20)
                if response.status_code == 200:
                    movie_data = response.json()
                    print(f"Movie data fetched: {movie_data}")
                download_link = scrape_torrent_link(movie_name)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching movie data: {e}")

    return render(request, 'search.html', {'form': form, 'movie_data': movie_data, 'download_link': download_link})

def scrape_torrent_link(movie_name):
    try:
        print(f"Searching for download link for: {movie_name}")
        search_url = f"https://en.ytsrs.com/movies/={movie_name.replace(' ', '+')}"
        response = requests.get(search_url, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Adjust the selector based on the site's HTML structure
        result = soup.find('a', class_='download-link-class')
        
        if result:
            download_url = result['href']
            print(f"Download link found: {download_url}")
            return download_url
        else:
            print(f"No download link found for: {movie_name}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching download link: {e}")
    
    return None
