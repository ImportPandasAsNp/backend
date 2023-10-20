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

    for index,row in metadata.iterrows():
        if (row["country"]=="United States" or row["country"]=="India") and row["image_url"]=="url":
            data = get_movie_info(remove_first_word_if_in_list(row["title"],wordlist))

            if data is not None:
                print(data)
                if "image_url" in data:
                    metadata.at[index,"image_url"] = data["image_url"]
                
                if "imdb_rating" in data:
                    metadata.at[index,"imdb_rating"] = data["imdb_rating"]

            else:
                break
    metadata.to_csv('/Users/adityaganguly/college/Hackon/backend/finalmetadata.csv',index=False)

    # for index,row in metadata.iterrows():

if __name__ == "__main__":
    main()