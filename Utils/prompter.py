from dotenv import load_dotenv
import os

load_dotenv()
open_api_key = os.getenv("open_ai_api_key_2")

class Prompter():
    def __init__(self,apiKey):
        self.apiKey = apiKey
        self.system = False
        self.systemText = "You are an intelligent keyword extractor. Extract the director, cast, genre, plot and title from the following text. Do not suggest any names on your own, or distort the names. Do not add any punctuation to the keywords. If you don't find a keyword fill it with unknown. When u see the phrase 'show me a movie by', assume it means the actor, directed by will be specified separately for directors. Return in the following format { 'title': '',	'director': [],	'genre': [], 'cast': [], 'plot': '' }. Output as a json string. \ntitle: will be the title of the movie\ndirector: will be the list of the directors\ncast: will be the list of cast members\ngenre: will be the list of genres from the following list ['parody', 'cult', 'spyespionage', 'buddy', 'romance', 'music', 'historical', 'anthology', 'faith and spirituality', 'action', 'teen tv shows', 'tv shows', 'docuseries', 'animation', 'series', 'drama', 'adventure', 'documentary', 'medical', 'international', 'game show competition', 'reality', 'anime', 'horror', 'travel', 'talk show and variety', 'superhero', 'arts', 'talk show', 'entertainment', 'arthouse', 'young adult audience', 'spanish', 'sports', 'movies', 'scifi', 'british', 'mystery', 'biographical', 'korean', 'culture', 'romantic comedy', 'unscripted', 'coming of age', 'science nature', 'dance', 'policecop', 'fitness', 'comedy', 'suspense', 'scifi fantasy', 'science fiction', 'classic movies', 'kids', 'animals  nature', 'lifestyle', 'disaster', 'independent', 'soap opera melodrama', 'western', 'documentaries', 'family', 'fantasy', 'variety', 'survival', 'action adventure', 'concert film', 'thriller', 'lgbtq', 'special interest', 'crime', 'military and war'].\nplot: this is a string field, try to find any segments of the query that is relevant to plot information.\nFor every field mentioned above there is no compulsion to fill it. If not found mention unknown for title or plot or return empty list for genre, cast or director.\nwhatever you return please follow the format, even if nothing can be extracted return th json string with the above mentioned keys."

    def prompt(self,text):
        pass