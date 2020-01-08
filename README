## MusicLearn
A web app that utilizes sentiment analysis to determine the general mood of a song through it's lyrics. Based on this information, it finds songs with similar moods by similar artists. These are then suggested to the user with easy links to open in Spotify.

### Installation
```Python
prereq: PyLyrics, SKLearn, spotipy, pandas
```
- Ensure all prequisites are installed.
```Python
cd app2/music
python manage.py runserver
```
- Navigate to 127.0.0.1:8000 in your browser, enter a song, and wait for the algorithm to run

### How we built it
We used python with Django to create the app. We used NLTK's Vader Sentiment Analyzer to find moods of songs, which outputs a metric of sentiment of any given sentence. We used this value to determine overall moods of songs. We then used the Spotify API to find similar artists and combed through their songs, determining the mood of each, and then ultimately finding the most similar songs to the user's original choice

### TO-DO
Optimize our algorithm to reduce the amount of time it takes to find matches. Right now, it takes about thirty seconds and given more time, we can easily cut this down to five-ten. We will also add more to our UI, giving the user a cleaner experience.

