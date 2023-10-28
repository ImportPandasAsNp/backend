import openai, os, copy
from dotenv import load_dotenv
from Utils.helpers import *

load_dotenv()

openai.api_key = os.getenv("open_ai_api_key")
def parse(query): 
    prompt_req = [
        {
            "content": "You are a keyword extractor. Extract the director, cast, genre and title from the following text. Do not suggest any names on your own, or distort the names. Do not add any punctuation to the keywords. If you don't find a keyword fill it with unknown. When u see the phrase 'show me a movie by', assume it means the actor, directed by will be specified separately. Try to classify query into genres 'parody', 'cult', 'spyespionage', 'buddy', 'romance', 'music', 'historical', 'anthology', 'faith and spirituality', 'action', 'teen tv shows', 'tv shows', 'docuseries', 'animation', 'series', 'drama', 'adventure', 'documentary', 'medical', 'international', 'game show competition', 'reality', 'anime', 'horror', 'travel', 'talk show and variety', 'superhero', 'arts', 'talk show', 'entertainment', 'arthouse', 'young adult audience', 'spanish', 'sports', 'movies', 'scifi', 'british', 'mystery', 'biographical', 'korean', 'culture', 'romantic comedy', 'unscripted', 'coming of age', 'science nature', 'dance', 'policecop', 'fitness', 'comedy', 'suspense', 'scifi fantasy', 'science fiction', 'classic movies', 'kids', 'animals  nature', 'lifestyle', 'disaster', 'independent', 'soap opera melodrama', 'western', 'documentaries', 'family', 'fantasy', 'variety', 'survival', 'action adventure', 'concert film', 'thriller', 'lgbtq', 'special interest', 'crime', 'military and war' however this is no compulsion and classify into unknown if not possible. Genre should only be the keywords provided or unknown. Output only a single genre type for each query. Format will be Title: <title>\nDirector: <director>\nCast: <list of cast members>\nGenre: <genre>",
            "role": "system"
        },
        {
            "content": query,
            "role": "user"
        }
    ]
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt_req
    )

    parsed_text = completion.choices[0].message.content
    print("qq", parsed_text)
    parsed_fields = parsed_text.lower().split("\n")
    req = dict()
    for item in parsed_fields:
        tmp = item.split(":")
        val = tmp[1].strip().split(", ")
        if len(val) == 1:
            if val[0] != "unknown":
                req.setdefault(tmp[0].strip(), val[0])
            continue

        req.setdefault(tmp[0].strip(), val)
    
    return req

# def mergeContext(previous: dict, current: dict):
#     curr_keys = current.keys()
#     prev_keys = previous.keys()
#     res = copy.deepcopy(current)
#     for key in curr_keys:
#         if key == "title" or key == "director":
#             continue
#         if type(current[key]) == "str":
#             res[key] = [current[key]]
#         if key in prev_keys:
#             res[key].extend(previous[key])
    
#     for key in previous.keys():
#         if key not in curr_keys:
#             res.setdefault(key, previous[key])

    
#     return res

x = {
    "title": "inception",
    "director": "unknown",
    "cast":["caprio"],
    "genre":["comedy"]
}

y = {
    "title": "intrstellar",
    "director": "nolan",
    "cast":[],
    "genre": "thriller"
}

r = mergeContext(x, y)
print(y)
print(r)

# r1 = parse("show me a movie by samuel l jackson and leonardo di caprio")
# r2 = parse("show me action, suspense and horror")
r0=dict()
r1={'cast': ['samuel l jackson', 'leonardo di caprio']}
r2={'genre': ['action', 'suspense', 'horror']}
r01=mergeContext(r0, r1)
r3 = mergeContext(r01, r2)
print(r01)
print(r1)
print(r2)
print(r3)