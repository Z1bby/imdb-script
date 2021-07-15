import requests
import random
from bs4 import BeautifulSoup

BASE = "http://localhost:5000/"
imdb_url = "https://www.imdb.com/chart/top"

def main():
    # getting html from imdb webpage
    response = requests.get(imdb_url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    # reading movie data from selected tags
    movietags = soup.select("td.titleColumn")
    inner_movietags = soup.select("td.titleColumn a")
    rating_tags = soup.select("td.posterColumn span[name=ir]")

    def get_year(movie_tag):
        moviesplit = movie_tag.text.split()
        year = moviesplit[-1]
        return year

    # saving data to arrays
    years = [get_year(tag) for tag in movietags]
    actors_list = [tag["title"] for tag in inner_movietags]
    titles = [tag.text for tag in inner_movietags]
    ratings = [float(tag["data-value"]) for tag in rating_tags]
    
    n_movies = len(titles)

    # adding random movie
    def add():
        idx = random.randrange(0, n_movies)
        print("adding <" + str(idx) + ">")
        protected = "True" if idx % 2 == 0 else "False"
        movie = {"title": titles[idx], "year": years[idx], "rating": f"{ratings[idx]:.1f}", "actors": actors_list[idx], "protected": protected}
        response = requests.put(BASE + "movie/" + str(idx), movie)
        print(response.json())

    # deleting movie with given id
    def delete(id):
        print("deleteing <" + str(id) + ">")
        response = requests.delete(BASE + "movie/" + str(id))

    # menu:
    print("add - adds new random movie",
        "delete <id> - deletes specified movie",
        "q - quits", sep="\n")
    while(True):
        user_input = input("action: ")
        user_args = user_input.split()
        
        if user_args[0] == "add":
            add()
        elif user_args[0] == "delete":
            delete(user_args[1])
        elif user_args[0] == "q":
            break

if __name__ == "__main__":
    main()
