from Utils.helpers import *

# x = {
#     "title": "inception",
#     "director": "unknown",
#     "cast":["caprio"],
#     "genre":["comedy"]
# }

# y = {
#     "title": "intrstellar",
#     "director": "nolan",
#     "cast":[],
#     "genre": "thriller"
# }

# r = mergeContext(x, y)
# print(y)
# print(r)

# # r1 = parse("show me a movie by samuel l jackson and leonardo di caprio")
# # r2 = parse("show me action, suspense and horror")
# r0=dict()
# r1={'cast': ['samuel l jackson', 'leonardo di caprio']}
# r2={'genre': ['action', 'suspense', 'horror']}
# r01=mergeContext(r0, r1)
# r3 = mergeContext(r01, r2)
# print(r01)
# print(r1)
# print(r2)
# print(r3)

t1={
  "title": "unknown",
  "director": [],
  "genre": [],
  "cast": ["Shah Rukh Khan"],
  "plot": "He takes part in a dance competition and steals a diamond."
}
t2={
  "title": "unknown",
  "director": [],
  "genre": ["action"],
  "cast": ["Tom Cruise"],
  "plot": "He jumps off a very tall building in the desert."
}

# print(mergeContext(t1, t2))
from UserChatContext.mem_db import userChatClient
userChatClient.getClient()
r1 = userChatClient.addContext("1", t1)
print(r1)
r2 = userChatClient.addContext("1", t2)
print(r2)