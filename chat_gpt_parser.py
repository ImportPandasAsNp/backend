from Utils.helpers import *


t0={
  "title": "unknown",
  "director": [],
  "genre": [],
  "cast": [],
  "plot": "unknown"
}

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
t3={
  "title": "unknown",
  "director": [],
  "genre": [],
  "cast": ["Leonardo DiCaprio", "Tom Hardy"],
  "plot": "unknown"
}
t4={
  "title": "unknown",
  "director": ["Nolan"],
  "genre": ["action", "thriller"],
  "cast": ["Christian Bale", "Hugh Jackman"],
  "plot": "They are magicians."
}


# print(mergeContext(t1, t2))
from UserChatContext.mem_db import userChatClient
userChatClient.getClient()
r1 = userChatClient.addContext("1", t1)
q1 = getQuery(r1)
print(r1, q1)
r1 = userChatClient.addContext("1", t2)
q1 = getQuery(r1)
print(r1, q1)
r1 = userChatClient.addContext("1", t3)
q1 = getQuery(r1)
print(r1, q1)
r1 = userChatClient.addContext("1", t4)
q1 = getQuery(r1)
print(r1, q1)
r1 = userChatClient.addContext("1", t4)
q1 = getQuery(r1)
print(r1, q1)

# userChatClient.removeContext("1")
# r1 = userChatClient.addContext("1", t4)
# print(r1)
# r1 = userChatClient.addContext("1", t3)
# print(r1)
# r1 = userChatClient.addContext("1", t2)
# print(r1)
# r1 = userChatClient.addContext("1", t1)
# print(r1)

q1 = getQuery(r1)