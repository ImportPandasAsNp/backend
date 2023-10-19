req = [
    {
        "content": "You are a keyword extractor",
        "role": "user"
    },
    {
        "content": "Inception is a 2010 science fiction action film[4][5][6] written and directed by Christopher Nolan, who also produced the film with Emma Thomas, his wife. The film stars Leonardo DiCaprio as a professional thief who steals information by infiltrating the subconscious of his targets. He is offered a chance to have his criminal history erased, as payment for the implantation of another person's idea into a target's subconscious.[7] The ensemble cast includes Ken Watanabe, Joseph Gordon-Levitt, Marion Cotillard, Elliot Page,[a] Tom Hardy, Cillian Murphy, Tom Berenger, Dileep Rao and Michael Caine.",
        "role": "user"
    },
    {
        "content": "extract the director, cast, genre and title from the text",
        "role": "user"
    }
]

import requests
import os
from dotenv import load_dotenv

load_dotenv()

# url=os.getenv("chat_gpt_url")
# rapid_api_key=os.getenv("X-RapidAPI-Key")
# rapid_api_host=os.getenv("X-RapidAPI-Host")
# custom_header = {"content-type": "application/json", "X-RapidAPI-Key":rapid_api_key, "X-RapidAPI-Host":rapid_api_host}
# r = requests. post(url=url, headers = custom_header, data=req)

url="https://dummyjson.com/products/add"
custom_header = {"content-type": "application/json"}
res = requests.post(url=url, headers=custom_header, data={"title":"random phone"})
print(res.text)
