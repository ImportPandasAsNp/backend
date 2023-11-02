# from Utils.helpers import *
# import openai, os
# from dotenv import load_dotenv
# load_dotenv()

# k=0


# t0={
#   "title": "unknown",
#   "director": [],
#   "genre": [],
#   "cast": [],
#   "plot": "unknown"
# }

# t1={
#   "title": "unknown",
#   "director": [],
#   "genre": [],
#   "cast": ["Shah Rukh Khan"],
#   "plot": "He takes part in a dance competition and steals a diamond."
# }
# t2={
#   "title": "unknown",
#   "director": [],
#   "genre": ["action"],
#   "cast": ["Tom Cruise"],
#   "plot": "He jumps off a very tall building in the desert."
# }
# t3={
#   "title": "unknown",
#   "director": [],
#   "genre": [],
#   "cast": ["Leonardo DiCaprio", "Tom Hardy"],
#   "plot": "unknown"
# }
# t4={
#   "title": "unknown",
#   "director": ["Nolan"],
#   "genre": ["action", "thriller"],
#   "cast": ["Christian Bale", "Hugh Jackman"],
#   "plot": "They are magicians."
# }


# # print(mergeContext(t1, t2))
# from UserChatContext.mem_db import userChatClient
# # userChatClient.getClient()
# # r1 = userChatClient.addContext("1", t1)
# # q1 = getQuery(r1)
# # print(r1, q1)
# # r1 = userChatClient.addContext("1", t2)
# # q1 = getQuery(r1)
# # print(r1, q1)
# # r1 = userChatClient.addContext("1", t3)
# # q1 = getQuery(r1)
# # print(r1, q1)
# # r1 = userChatClient.addContext("1", t4)
# # q1 = getQuery(r1)
# # print(r1, q1)
# # r1 = userChatClient.addContext("1", t4)
# # q1 = getQuery(r1)
# # print(r1, q1)

# def parse(query: str):
#   global k
#   openai.api_key = os.getenv(f"open_ai_api_key_{2}")
#   k += 1
#   print(openai.api_key)
#   prompt_req = [
#       {
#           "content": "You are an intelligent keyword extractor. Extract the director, cast, genre, plot and title from the following text. Do not suggest any names on your own, or distort the names. Do not add any punctuation to the keywords. If you don't find a keyword fill it with unknown. When u see the phrase 'show me a movie by', assume it means the actor, directed by will be specified separately for directors. Return in the following format { 'title': '',	'director': [],	'genre': [], 'cast': [], 'plot': '' }. Output as a json string. \ntitle: will be the title of the movie\ndirector: will be the list of the directors\ncast: will be the list of cast members\ngenre: will be the list of genres from the following list ['parody', 'cult', 'spyespionage', 'buddy', 'romance', 'music', 'historical', 'anthology', 'faith and spirituality', 'action', 'teen tv shows', 'tv shows', 'docuseries', 'animation', 'series', 'drama', 'adventure', 'documentary', 'medical', 'international', 'game show competition', 'reality', 'anime', 'horror', 'travel', 'talk show and variety', 'superhero', 'arts', 'talk show', 'entertainment', 'arthouse', 'young adult audience', 'spanish', 'sports', 'movies', 'scifi', 'british', 'mystery', 'biographical', 'korean', 'culture', 'romantic comedy', 'unscripted', 'coming of age', 'science nature', 'dance', 'policecop', 'fitness', 'comedy', 'suspense', 'scifi fantasy', 'science fiction', 'classic movies', 'kids', 'animals  nature', 'lifestyle', 'disaster', 'independent', 'soap opera melodrama', 'western', 'documentaries', 'family', 'fantasy', 'variety', 'survival', 'action adventure', 'concert film', 'thriller', 'lgbtq', 'special interest', 'crime', 'military and war'].\nplot: this is a string field, try to find any segments of the query that is relevant to plot information.\nFor every field mentioned above there is no compulsion to fill it. If not found mention unknown for title or plot or return empty list for genre, cast or director.\nwhatever you return please follow the format, even if nothing can be extracted return th json string with the above mentioned keys. Another important thing is the text may  be in some language other than english, but written in english. You are to translate it to english",
#           "role": "system"
#       },
#       {
#           "content": query,
#           "role": "user"
#       }
#   ]
#   completion = openai.ChatCompletion.create(
#       model="gpt-3.5-turbo",
#       messages=prompt_req
#   )

#   res = completion.choices[0].message.content
#   return res

# r1=parse("action movies starring srk")
# print(r1)
# r1=parse("thriller movie with a tragic ending where tom cruise dies")
# print(r1)


import signal

# Register an handler for the timeout
def handler(signum, frame):
   print("gg")
   raise Exception("end of time")

# This function *may* run for an indetermined time...
def loop_forever():
   while True:
      pass
   
   return True


def query():
  # Register the signal function handler
  signal.signal(signal.SIGALRM, handler)

  # Define a timeout for your function
  signal.alarm(5)

  try:
    res = loop_forever()
  except Exception as e:
    print(e)

query()