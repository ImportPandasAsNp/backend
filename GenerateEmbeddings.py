import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import tensorflow as tf
import numpy as np
import os
import glob
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import Dataset, DataLoader
import shutil
import pandas as pd
import random
import math
from sklearn.model_selection import StratifiedKFold, KFold
from PIL import Image
import copy
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

def jenkins_hash(s):
    hash = 0
    for c in s:
        hash += ord(c)
        hash += (hash << 10)
        hash ^= (hash >> 6)

    hash += (hash << 3)
    hash ^= (hash >> 11)
    hash += (hash << 15)

    # Ensure the hash is a non-negative integer
    hash &= 0xFFFFFFFFFFFFFFFF  # 64-bit hash
    return hash


import string
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download the WordNet corpus
nltk.download('punkt')
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()

def preprocessText(text):
    """
    Preprocesses the input text by removing punctuation, converting to lowercase, and lemmatizing.

    Parameters:
    text (str): Input text to be preprocessed.

    Returns:
    str: Preprocessed text.
    """
    text = text.translate(str.maketrans("", "", string.punctuation))

    text = text.lower()

    words = word_tokenize(text)
    lemmatized_words = [lemmatizer.lemmatize(word, wordnet.VERB) for word in words]
    preprocessed_text = ' '.join(lemmatized_words)

    return preprocessed_text


hotstar = pd.read_csv("/content/drive/My Drive/Hackon2023/Datasets/disney_plus_titles.csv")
prime = pd.read_csv("/content/drive/My Drive/Hackon2023/Datasets/amazon_prime_titles.csv")
netflix = pd.read_csv("/content/drive/My Drive/Hackon2023/Datasets/netflix_titles.csv")
print("The Conjuring" in hotstar["title"])

hotstar["platform"] = ["hotstar" for i in range(len(hotstar))]
prime["platform"] = ["prime" for i in range(len(prime))]
netflix["platform"] = ["netflix" for i in range(len(netflix))]

movieData = pd.concat([hotstar, prime, netflix])
movieData["imdb_rating"] = ["1" for i in range(len(movieData))]

movieData["id"] = [jenkins_hash(s) for s in movieData["title"]]

# movieData.drop(movieData[movieData["release_year"]<2005].index,inplace=True)

movieData = movieData[(movieData['country'] == 'India') | (movieData['country'] == 'United States')]
movieData.drop(["duration", "show_id","date_added"], axis = 1, inplace = True)

movieData["director"] = movieData["director"].fillna("unknown")
movieData["title"] = movieData["title"].fillna("unknown")
movieData["listed_in"] = movieData["listed_in"].fillna("unknown")
movieData["cast"] = movieData["cast"].fillna("unknown")

def removePunctuationAndLowerCase(text):
    translator = str.maketrans('', '', ''.join([char for char in string.punctuation if char != ',']))
    text_without_punctuations = text.translate(translator)
    text_lowercase = text_without_punctuations.lower()

    return text_lowercase

def commaStringToList(x):
    elements = x.split(',')
    return [elem.strip() for elem in elements if elem]

movieData["director"] = movieData["director"].apply(lambda x: removePunctuationAndLowerCase(x))
movieData["listed_in"] = movieData["listed_in"].apply(lambda x: removePunctuationAndLowerCase(x))
movieData["cast"] = movieData["cast"].apply(lambda x: removePunctuationAndLowerCase(x))

movieData["director"] = movieData["director"].apply(lambda x: commaStringToList(x))
movieData["listed_in"] = movieData["listed_in"].apply(lambda x: commaStringToList(x))
movieData["cast"] = movieData["cast"].apply(lambda x: commaStringToList(x))

genreDict = {
    'animation': 'animation',
    'family': 'family',
    'comedy': 'comedy',
    'musical': 'music',
    'docuseries': 'docuseries',
    'historical': 'historical',
    'music': 'music',
    'biographical': 'biographical',
    'documentary': 'documentary',
    'actionadventure': 'action adventure',
    'superhero': 'superhero',
    'reality': 'reality',
    'survival': 'survival',
    'animals  nature': 'animals  nature',
    'kids': 'kids',
    'coming of age': 'coming of age',
    'drama': 'drama',
    'fantasy': 'fantasy',
    'lifestyle': 'lifestyle',
    'movies': 'movies',
    'science fiction': 'science fiction',
    'concert film': 'concert film',
    'crime': 'crime',
    'sports': 'sports',
    'anthology': 'anthology',
    'medical': 'medical',
    'variety': 'variety',
    'spyespionage': 'spyespionage',
    'buddy': 'buddy',
    'parody': 'parody',
    'game show  competition': 'game show competition',
    'romance': 'romance',
    'anime': 'anime',
    'romantic comedy': 'romantic comedy',
    'thrillers': 'thriller',  # Merged 'tv thriller' and 'thrillers'
    'policecop': 'policecop',
    'talk show': 'talk show',
    'western': 'western',
    'dance': 'dance',
    'series': 'series',
    'mystery': 'mystery',
    'soap opera  melodrama': 'soap opera melodrama',
    'disaster': 'disaster',
    'travel': 'travel',
    'international': 'international',
    'action': 'action',
    'suspense': 'suspense',
    'special interest': 'special interest',
    'adventure': 'adventure',
    'horror': 'horror',
    'talk show and variety': 'talk show and variety',
    'arts': 'arts',
    'entertainment': 'entertainment',
    'and culture': 'culture',
    'tv shows': 'tv shows',
    'music videos and concerts': 'music',
    'fitness': 'fitness',
    'faith and spirituality': 'faith and spirituality',
    'military and war': 'military and war',
    'lgbtq': 'lgbtq',
    'unscripted': 'unscripted',
    'young adult audience': 'young adult audience',
    'arthouse': 'arthouse',
    'documentaries': 'documentaries',
    'international tv shows': 'international',
    'tv dramas': 'drama',
    'tv mysteries': 'mystery',
    'crime tv shows': 'crime',
    'tv action  adventure': 'action adventure',
    'reality tv': 'reality',
    'romantic tv shows': 'romance',
    'tv comedies': 'comedy',
    'tv horror': 'horror',
    'children  family movies': 'family',
    'dramas': 'drama',
    'independent movies': 'independent',
    'international movies': 'international',
    'british tv shows': 'british',
    'comedies': 'comedy',
    'spanishlanguage tv shows': 'spanish',
    'romantic movies': 'romance',
    'music  musicals': 'music',
    'scifi fantasy': 'scifi fantasy',
    'tv scifi fantasy':'scifi fantasy',
    'kids tv': 'kids',
    'action  adventure': 'action adventure',
    'classic movies': 'classic movies',
    'anime features': 'anime',
    'sports movies': 'sports',
    'anime series': 'anime',
    'korean tv shows': 'korean',
    'science  nature tv': 'science nature',
    'teen tv shows': 'teen tv shows',
    'cult movies': 'cult',
    'faith  spirituality': 'faith and spirituality',
    'lgbtq movies': 'lgbtq',
    'standup comedy': 'comedy',
    'standup comedy  talk shows': 'comedy',
    'classic  cult tv': 'cult',
    'horror movies':'horror',
    'tv thrillers':'thriller',
    'scifi  fantasy':'scifi',
    'tv scifi  fantasy':'scifi',
    'thriller':'thriller'

}

movieData["listed_in"] = movieData["listed_in"].apply(lambda x: [genreDict[elem] for elem in x])
movieData["listed_in"] = movieData["listed_in"].apply(lambda x: ",".join(x))
movieData["director"] = movieData["director"].apply(lambda x: ",".join(x))
movieData["cast"] = movieData["cast"].apply(lambda x: ",".join(x))
movieData.rename(columns = {"listed_in":"genre"}, inplace=True)

from langchain.embeddings import SentenceTransformerEmbeddings
embeddings = SentenceTransformerEmbeddings(model_name="sentence-transformers/clip-ViT-B-32-multilingual-v1")

from sentence_transformers import SentenceTransformer, util
EMB_DIM = 512
MOVIES = len(movieData)
movieDict = dict()

for index, row in movieData.iterrows():
    # genreemb = embeddings.embed_query(" ".join(row["listed_in"]))
    if row["title"] in movieDict:
      continue
    genretxt = " ".join(row['genre'].split(','))
    descemb = embeddings.embed_query("title " + row["title"] + " genre list " + genretxt + " description " + row["description"])
    descemb = torch.as_tensor(descemb)
    movieDict[row["title"]] = descemb


feats = pd.DataFrame()
idDict = dict(zip(list(movieData["id"]),[movieDict[t].tolist() for t in list(movieData["title"]) ]))
feats["id"] = movieData["id"]
feats["feature"] = [idDict[id] for id in movieData["id"]]

# feats = feats.sample(frac=0.15, index=False)
feats.to_csv("/content/drive/My Drive/Hackon2023/Datasets/feats2.csv")

relations = ["genre", "actor", "director"]
genreGraph = dict()
actorGraph = dict()
directorGraph = dict()

for index, row in movieData.iterrows():

  for genre in row["genre"]:
    if genre not in genreGraph.keys():
      genreGraph[genre] = list()

    genreGraph[genre].append(row["title"])

  for director in row["director"]:
    if director not in directorGraph.keys():
      directorGraph[director] = list()

    directorGraph[director].append(row["title"])

  for actor in row["cast"]:
    if actor not in actorGraph.keys():
      actorGraph[actor] = list()

    actorGraph[actor].append(row["title"])


data = {'from': [''], 'to': [''], 'rel': ['']}
graphDataFrame = pd.DataFrame(data)

def insertEntireDict(d, rel, graphDataFrame):
  data = []
  for key in d.keys():
    for lis in d[key]:
      data.append({'from':key, 'to':lis, 'rel':rel})
  return graphDataFrame.append(data, ignore_index = True)

graphDataFrame = insertEntireDict(actorGraph,"actor", graphDataFrame)
graphDataFrame = insertEntireDict(directorGraph,"director", graphDataFrame)
graphDataFrame = insertEntireDict(genreGraph,"genre", graphDataFrame)
graphDataFrame = graphDataFrame.sample(frac = 1)
graphDataFrame.drop(graphDataFrame[graphDataFrame["from"]=="unknown"].index,inplace=True)

torchKGData = torchkge.KnowledgeGraph(df=graphDataFrame)

import torchkge
from torchkge.models.bilinear import ComplExModel
from torchkge.models.deep import ConvKBModel
from torchkge.sampling import BernoulliNegativeSampler
from torchkge.utils import MarginLoss, DataLoader

from torchkge.models.translation import TransDModel,TransRModel
from torch import ones_like, zeros_like
from torch.nn import Module, Sigmoid
from torch.nn import MarginRankingLoss, SoftMarginLoss, BCELoss
from tqdm import tqdm

embeddingDimension = 128
learningRate = 0.0001
numEpochs = 10000
batchSize = 256
margin = 0.5

class MarginLoss(Module):
    """Margin loss as it was defined in `TransE paper
    <https://papers.nips.cc/paper/5071-translating-embeddings-for-modeling-multi-relational-data>`_
    by Bordes et al. in 2013. This class implements :class:`torch.nn.Module`
    interface.

    """
    def __init__(self, margin):
        super().__init__()
        self.loss = MarginRankingLoss(margin=margin, reduction='none')

    def forward(self, positive_triplets, negative_triplets,weights):
        """
        Parameters
        ----------
        positive_triplets: torch.Tensor, dtype: torch.float, shape: (b_size)
            Scores of the true triplets as returned by the `forward` methods of
            the models.
        negative_triplets: torch.Tensor, dtype: torch.float, shape: (b_size)
            Scores of the negative triplets as returned by the `forward`
            methods of the models.

        Returns
        -------
        loss: torch.Tensor, shape: (n_facts, dim), dtype: torch.float
            Loss of the form
            :math:`\\max\\{0, \\gamma - f(h,r,t) + f(h',r',t')\\}` where
            :math:`\\gamma` is the margin (defined at initialization),
            :math:`f(h,r,t)` is the score of a true fact and
            :math:`f(h',r',t')` is the score of the associated negative fact.
        """
        return torch.mean(weights * self.loss(positive_triplets, negative_triplets,
                         target=ones_like(positive_triplets)))

complexModel = TransRModel(ent_emb_dim=embeddingDimension,rel_emb_dim = embeddingDimension, n_entities=torchKGData.n_ent, n_relations=torchKGData.n_rel)
criterion = MarginLoss(margin)

optimizer = torch.optim.Adam(complexModel.parameters(), lr=learningRate)
sampler = BernoulliNegativeSampler(torchKGData)
dataloader = DataLoader(torchKGData, batch_size=256, use_cuda="batch")

if torch.cuda.is_available():
    torch.cuda.empty_cache()
    complexModel.cuda()
    criterion.cuda()

iterator = tqdm(range(numEpochs), unit='epoch')

for epoch in iterator:
    runningLoss = 0.0
    cnt = 0
    for i,batch in enumerate(dataloader):

        if random.random() < 1.0:
          cnt+=1
          head, tail, relation = batch[0], batch[1], batch[2]
          # print(relation)
          numHead, numTail = sampler.corrupt_batch(head, tail, relation)
          optimizer.zero_grad()
          pos, neg = complexModel(head, tail, relation, numHead, numTail)
          weights = (relation == 3) + 1

          loss = criterion(pos, neg,weights)
          loss.backward()
          optimizer.step()
          runningLoss += loss.item()
    iterator.set_description('Epoch %d, loss %.5f' % (epoch, runningLoss/cnt))