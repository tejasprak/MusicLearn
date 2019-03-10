# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import tform
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext

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
def get_artist_id(name):
    client_credentials_manager = SpotifyClientCredentials(client_id='6d97c2f902d54748a76360adf94c0c9b', client_secret='44bc5c4bbc22479a984d747e20e0ba48')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
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

@csrf_exempt
def index(request):
    #print listdir('.')
    firstName = ''
    lastName = ''
    context = RequestContext(request)
    context_dict = {}
    context_dict['LUL'] = "DRAFT"
    cd = {}
    if request.method == "POST":
        f = tform(request.POST)
        if f.is_valid():
            cd = f.cleaned_data
            initial_artist=cd['artist']
            artist_list=[initial_artist]
            initial_song=cd['song']
            lyrics = PyLyrics.getLyrics(initial_artist,initial_song)
            initial = find_percent(lyrics)[0]
            client_credentials_manager = SpotifyClientCredentials(client_id='6d97c2f902d54748a76360adf94c0c9b', client_secret='44bc5c4bbc22479a984d747e20e0ba48')
            sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
            rec_songs=[]
            artist_names=[]
            names_songs={}
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
            b=0
            for song in rec_songs:
                names_songs[song]=artist_names[b]
                print names_songs
                b=b+1
            print names_songs
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
            top=[]
            links=[]
            z=0
            for key, value in sorted(difference.iteritems(), key=lambda (k,v): (v,k)):
                if z<4:
                    print "%s: %s" % (key, value)
                    link = sp.search(str(key), limit=1, offset=0, type='track', market=None)
                    link =  link['tracks']['items'][0]['external_urls']['spotify']
                    links.append(link)
                    top.append(str(key) + " by " + str(names_songs[key]))
            context_dict['bool']="existence"
            context_dict['one']=top[0]
            context_dict['two']=top[1]
            context_dict['three']=top[2]
            context_dict['four']=top[3]
            context_dict['five']=top[4]
            context_dict['linkone']=links[0]
            context_dict['linktwo']=links[1]
            context_dict['linkthree']=links[2]
            context_dict['linkfour']=links[3]
            context_dict['linkfive']=links[4]
            context_dict['recstring']="Top 5 Recommended Songs!"
    else:
        f = tform()
        args = {}
        args['form'] = f
    context_dict['form'] = f

    return render_to_response('musiclearn/index.html', context_dict, context)
