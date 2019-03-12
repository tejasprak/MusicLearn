#SONG RECOMMENDATION

import re
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from PyLyrics import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')
artist_list=["DRAM"]
initial_song="Broccoli"
initial_artist="DRAM"
def get_artist_id(name):
    id=sp.search(q=name, type="artist", limit=10)
    id= id['artists']['items'][0]['id']
    return id
def find_percent(string):
    newfile = []
    chorusfound = False
    for line in string.split("\n"):
        newfile.append(line)
    lyrics = newfile
    for line in lyrics:
        line = re.sub(r'[\(\[].*?[\)\]]', '', line)


    df = pd.DataFrame(columns=('artist', 'pos', 'neu', 'neg'))
    sid = SentimentIntensityAnalyzer()
    i=0
    num_positive = 0
    num_negative = 0
    num_neutral = 0
    for sentence in lyrics:
        if sentence:
            #print sentence
            this_sentence = sentence.decode('utf-8')
            comp = sid.polarity_scores(this_sentence)
            comp = comp['compound']
            comp = float(comp)
            #print comp
            if comp>0:
                num_positive += 1
            elif comp<0:
                num_negative += 1
    num_total = num_negative + num_neutral + num_positive
    negative = (float(num_negative)/float(num_total))
    positive = (float(num_positive)/float(num_total))
    return [positive, negative]

lyrics = PyLyrics.getLyrics(initial_artist,initial_song)
initial = find_percent(lyrics)[0]

client_credentials_manager = SpotifyClientCredentials(client_id='', client_secret='')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

rec_songs=[]
artist_names=[]
for artist in artist_list:
    id=get_artist_id(artist)
    related = sp.artist_related_artists(id)
    for name in related['artists']:
        name=name['name']
        print name
        id2=get_artist_id(name)
        for track in sp.artist_top_tracks(id2, country='US')['tracks']:
            rec_songs.append(track["name"])
            artist_names.append(name)
i=0
lyrics = PyLyrics.getLyrics("Juice WRLD","Empty")
sentiments = {}
for song in rec_songs:
    try:
        lyrics = PyLyrics.getLyrics(artist_names[i],song)
        sentiment = find_percent(lyrics)
        #print song, " ", artist_names[i]
        sentiments[song]=sentiment[0]
        #print sentiment[0]
    except ValueError:
        #print song
        print 'Invalid value!'
    i=i+1
difference={}
for song,value in sentiments.iteritems():
    difference_current=abs(initial-value)
    difference[song] = difference_current
for key, value in sorted(difference.iteritems(), key=lambda (k,v): (v,k)):
    print "%s: %s" % (key, value)
