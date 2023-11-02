import requests
import pandas as pd
api_key = "f659e1f"
wordlist = ['Marvel','Marvels','Disney','Disneys']

import requests
from bs4 import BeautifulSoup
import wikipedia

import string
from nltk.stem import WordNetLemmatizer

def process_text(text):
    # Remove punctuation
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)

    # Lowercase the text
    text = text.lower()

    # Lemmatize the text
    lemmatizer = WordNetLemmatizer()
    words = text.split()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]

    # Join the lemmatized words back into a single string
    processed_text = ' '.join(lemmatized_words)

    return processed_text

def find_similar_wikipedia_page(query):
    try:
        # Attempt to get the Wikipedia page for the exact query
        page = wikipedia.page(query)
        return page.url
    except wikipedia.exceptions.DisambiguationError as e:
        # If there are disambiguation options, return the first one
        try:
            return wikipedia.page(e.options[0]).url
        except:
            return None
    except wikipedia.exceptions.HTTPTimeoutError:
        return None
    except wikipedia.exceptions.PageError:
        return None
    except Exception as e:
        return None

# def find_similar_wikipedia_page(query):
#     # Create a Wikipedia API object
#     wiki_wiki = wikipediaapi.Wikipedia(language="en",user_agent='CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)')

#     # Try to get the Wikipedia page for the exact query
#     exact_page = wiki_wiki.page(query)

#     if exact_page.exists():
#         return exact_page.fullurl

#     # If the exact page doesn't exist, search for similar pages
#     search_results = wiki_wiki.page(f"Special:Search/{query}", unquote=False)
#     print(search_results)
#     if search_results.exists():
#         # Get the title and full URL of the most relevant search result
#         most_relevant_result = search_results.links[0]
#         return most_relevant_result.fullurl

#     return None

def get_movie_plot_summary(movie_name):

    wiki_url = find_similar_wikipedia_page(movie_name)

    if wiki_url is None:
        return "No plot found"

    print(wiki_url)
    try:
        # Specify a valid user agent in the headers
        headers = {'User-Agent': 'CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)'}

        # Fetch the Wikipedia page content using the URL and user agent
        response = requests.get(wiki_url, headers=headers)

        if response.status_code == 200:
            # print(response.text)
            soup = BeautifulSoup(response.text, 'html.parser')
            # print(soup)
            # Find the section containing the plot summary
            plot_section = soup.find('span', {'id': 'Plot'})
  
            if plot_section:
                # Extract the plot summary text
                plot_summary = ""
                plot_section = plot_section.find_parent('h2')
                for sibling in plot_section.find_next_siblings():
                    if sibling.name and sibling.name.startswith('h'):
                        break
                    if sibling.name == 'p':
                        plot_summary += sibling.get_text()

                if plot_summary:
                    plot_summary = plot_summary.replace("\n"," ")
                    return plot_summary.strip()
                else:
                    return "No plot found"
            else:
                return "No plot found"

        else:
            return "No plot found"

    except Exception as e:
        return f"Error: {str(e)}"

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
                'poster_url': poster_url,
                'original_title':movie['original_title']
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

        if 'original_title' in data:
            ret['original_title'] = data['original_title']

        return ret
    else:
        print("Failed to retrieve data from OMDB API")
        return None
    
def main():
    metadata = pd.read_csv('/Users/adityaganguly/college/Hackon/backend/finalmetadata.csv')

    temp = pd.read_csv('/Users/adityaganguly/college/Hackon/backend/modified2original.csv')
    metadata["plot"] = [" " for _ in range(len(metadata))]
    id2Og = dict(zip(temp["id"],temp["original_title"]))

    # metadata["description"] = ["t" for _ in range(len(metadata))]
    # idPlatform = dict()
    # idTitle = dict()
    # idDescription=dict()
    # newFrame = pd.DataFrame()

    # newFrame["id"] = metadata["id"]
    # newFrame["modified_title"] = metadata["title"]
    # newFrame["original_title"] = [" " for _ in range(len(metadata))]

    # idPlatform = dict(zip(temp["id"],temp["platform"]))
    # idTitle = dict(zip(temp["id"],temp["title"]))
    # idDescription = dict(zip(temp["id"],temp["description"]))

    for index,row in metadata.iterrows():
        # if (row["country"]=="United States" or row["country"]=="India"):
        # data = fetch_movie_info_by_name(remove_first_word_if_in_list(row["title"],wordlist))

        # if data is None:
        #     newFrame.at[index,'original_title'] = " "
        # else:
        #     newFrame.at[index,'original_title'] = data['original_title']
        #     print(data['original_title'])

        data = get_movie_plot_summary(id2Og[row["id"]])
        metadata.at[index,"plot"]=data
        # print(data)

        # metadata.at[index,"plot"] = process_text(metadata.at[index,"plot"])

        # break

        # if data is not None:
        #     print(data)
        #     if "poster_url" in data:
        #         metadata.at[index,"image_url"] = data["poster_url"]
        #         print(data["poster_url"])
            
        #     if "imdb_rating" in data:
        #         metadata.at[index,"imdb_rating"] = data["imdb_rating"]
        # metadata.at[index,"platform"] = idPlatform[row["id"]]
        # metadata.at[index,"title"] = idTitle[row["id"]]
        # metadata.at[index,"description"]=idDescription[row["id"]]


    # metadata.drop(metadata.index[indices],inplace=True)
    metadata.to_csv('/Users/adityaganguly/college/Hackon/backend/copyofdata.csv',index=False)
    

    # for index,row in metadata.iterrows():

if __name__ == "__main__":
    main()