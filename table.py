import unidecode
import string
import random
import re
import time
import math

from nltk.corpus import stopwords


file = open('gigaword-sample.flat')
english_corpus = []
for line in file:
  line = unidecode.unidecode(line)
  english_corpus.extend(line.split())
  
file = unidecode.unidecode(open('kanye.txt').read())
file = re.sub(r'\[.*\]', '', file)
file = re.sub(r'\n+', '\n', file)
first_split = file.split(' ')
next_split = []
for token in first_split:
  next_split.extend(re.findall(r"[\w']+|[\n]", token))
  
second_split = []
for token in next_split:
  if '\n' in token:
    splits = token.split('\n')
    for subtoken in splits[:-1]:
      second_split.extend([subtoken, '\n'])
    second_split.append(splits[-1])
  else:
    second_split.append(token)
    
kanye_corpus = second_split

vocab = list(set(kanye_corpus) | set(english_corpus))
n_vocab = len(vocab)

english_occurrances = dict()
kanye_occurrances = dict()
for word in english_corpus:
  english_occurrances[word] = english_occurrances.get(word, 0) + 1
for word in kanye_corpus:
  kanye_occurrances[word] = english_occurrances.get(word, 0) + 1
  
kanyeness = dict()
for word in set(kanye_corpus) & set(english_corpus):
  if kanye_occurrances[word] >= 5 and english_occurrances[word] >= 5:
    n_kanye = math.log(kanye_occurrances[word] / len(kanye_corpus))
    n_english = math.log(english_occurrances[word] / len(english_corpus))
    kanyeness[word] = n_kanye - n_english

blacklist = set(stopwords.words('english')) | {'', '\n'}
s = [(k) for k in sorted(kanyeness, key=kanyeness.get, reverse=True) if k not in blacklist]

# print(s[:10])
print('\n'.join(s[-10:]))
