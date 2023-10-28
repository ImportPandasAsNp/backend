import requests
from bs4 import BeautifulSoup
import wikipedia

def find_similar_wikipedia_page(query):
    try:
        # Attempt to get the Wikipedia page for the exact query
        page = wikipedia.page(query)
        return page.url
    except wikipedia.exceptions.DisambiguationError as e:
        # If there are disambiguation options, return the first one
        return wikipedia.page(e.options[0]).url
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


if __name__ == "__main__":
    # movie_name = "Pirates of the Caribbean: Dead Men Tell No Tales"  # Replace with the movie name you want to search
    # plot_summary = get_movie_plot_summary(movie_name)
    # print(f"Plot Summary of {movie_name}:\n{plot_summary}")
    print(process_text("Tallahassee steals his gun back and has a stand-off with Wichita, until Columbus intervenes saying that they have bigger problems to worry about, resulting in an uneasy truce between them. The sisters reveal they are going to the Pacific Playland amusement park in Los Angeles, an area supposedly free of zombies. After learning his hometown has been destroyed, and his parents likely killed, Columbus and Tallahassee decide to accompany them to the amusement park. When the group reach Hollywood, Tallahassee directs them to Bill Murray's house. Tallahassee and Wichita meet Murray, uninfected and disguised as a zombie"))
