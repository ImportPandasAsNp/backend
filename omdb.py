import requests
import pandas as pd
api_key = "f659e1f"
wordlist = ['marvel','marvels','disney','disneys']

def remove_first_word_if_in_list(input_string, word_list):
    # Split the input string into words
    words = input_string.split()

    if words[0]=="marvel" and words[1] == "studios":
        words.pop(0)
        words.pop(0)
    
    else:
    # Check if the first word is in the list
        if words and words[0] in word_list:
            # Remove the first word if it's in the list
            words.pop(0)
    
    # Join the remaining words back into a string
    updated_string = ' '.join(words)
    
    return updated_string

TMDB_API_KEY = 'a45d406e049179c48005a841d4d245f9'
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

# Function to fetch movie information by name
def fetch_movie_info_by_name(movie_name):
    try:
        # Make a search request for the movie by name
        search_params = {
            'api_key': TMDB_API_KEY,
            'query': movie_name
        }
        search_response = requests.get(f'{TMDB_BASE_URL}/search/movie', params=search_params)

        search_data = search_response.json()

        if search_data['results']:
            # Assuming the first result is the desired movie
            movie = search_data['results'][0]

            # Extract details like title, overview, and poster_path
            title = movie['title']
            overview = movie['overview']
            poster_path = movie['poster_path']

            # Construct the full poster URL
            poster_url = f'https://image.tmdb.org/t/p/w500{poster_path}'

            return {
                'title': title,
                'overview': overview,
                'poster_url': poster_url
            }
        else:
            return None  # Movie not found
    except Exception as e:
        print(f'Error fetching movie info: {e}')
        raise

def get_movie_info(movie_title):
    api_key = "37400cfc"  # Replace with your OMDB API key
    omdb_url = f"http://www.omdbapi.com/?apikey={api_key}&t={movie_title}"

    # Send a GET request to the OMDB API
    response = requests.post(omdb_url)
    print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        ret = dict()
        # Check if 'Poster' and 'imdbRating' keys are in the response
        if 'Poster' in data:
            ret["image_url"] = data['Poster']
        
        if 'imdbRating' in data:
            ret["imdb_rating"] = data['imdbRating']

        return ret
    else:
        print("Failed to retrieve data from OMDB API")
        return None
    
def main():
    metadata = pd.read_csv('/Users/adityaganguly/college/Hackon/backend/finalmetadata.csv')
    temp = pd.read_csv('/Users/adityaganguly/college/Hackon/backend/temp.csv')

    metadata["description"] = ["t" for _ in range(len(metadata))]
    idPlatform = dict()
    idTitle = dict()
    idDescription=dict()

    idPlatform = dict(zip(temp["id"],temp["platform"]))
    idTitle = dict(zip(temp["id"],temp["title"]))
    idDescription = dict(zip(temp["id"],temp["description"]))

    for index,row in metadata.iterrows():
        # if (row["country"]=="United States" or row["country"]=="India") and row["image_url"]=="https://occ-0-2365-2186.1.nflxso.net/dnm/api/v6/6gmvu2hxdfnQ55LZZjyzYR4kzGk/AAAABVXBb2OIJF5kpOGVZ5TNjIydKyVReN6qd6UC2BJGpHfU1KGl1eaCApGzqcdP6LzCYI1Vt2P8UYL2d7FTP4of0zggLAC7i8TlmTI.webp?r=841":
        # #     data = fetch_movie_info_by_name(remove_first_word_if_in_list(row["title"],wordlist))

        # #     if data is not None:
        # #         print(data)
        # #         if "poster_url" in data:
        # #             metadata.at[index,"image_url"] = data["poster_url"]
        # #             print(data["poster_url"])
                
        # #         if "imdb_rating" in data:
        # #             metadata.at[index,"imdb_rating"] = data["imdb_rating"]
        #     cnt+=1
        #     indices.append(index)
        metadata.at[index,"platform"] = idPlatform[row["id"]]
        metadata.at[index,"title"] = idTitle[row["id"]]
        metadata.at[index,"description"]=idDescription[row["id"]]


    # metadata.drop(metadata.index[indices],inplace=True)
    metadata.to_csv('/Users/adityaganguly/college/Hackon/backend/finalmetadata.csv',index=False)
    

    # for index,row in metadata.iterrows():

if __name__ == "__main__":
    main()