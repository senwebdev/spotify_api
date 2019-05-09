from bottle import route, run, request, get, post
import requests
import spotipy
import spotipy.util as util
from spotipy import oauth2
from spotipy.oauth2 import SpotifyClientCredentials 
import json
import codecs

username = '7g3ogpmibnroegln26j2w85yu'
port = 8080
scope = 'user-read-private user-read-birthdate user-read-email playlist-read-private user-library-read user-library-modify user-top-read playlist-read-collaborative playlist-modify-public playlist-modify-private user-follow-read user-follow-modify user-read-playback-state user-read-currently-playing user-modify-playback-state user-read-recently-played'
cid='71404b7d722145709fd49b08186cdc2d'
csecret='f38c6cbe73354243b7e30a566ab99136'
redirectURI='http://localhost:8080'
cache = '.spotipyoauthcache'

sp_oauth = oauth2.SpotifyOAuth( cid, csecret,redirectURI,scope=scope,cache_path=cache )

@route('/test')
def index():
    currentPlayingBtn = "<a href='/current-playing'>Current Playing</a><br>"
    userTopArtistsBtn = "<a href='/user-top-artists'>User Top Artists</a><br>"
    previousTrackBtn = ""
    recentlyPlayedBtn = "<a href='/recently-played'>Recently Played</a><br>"
    featuredPlaylistsBtn = "<a href='/featured-playlists'>Featured Playlists</a><br>"
    return currentPlayingBtn, userTopArtistsBtn, previousTrackBtn, recentlyPlayedBtn, featuredPlaylistsBtn

@route('/')
def auth():
        
    access_token = ""

    token_info = sp_oauth.get_cached_token()

    if token_info:
        print ("Found cached token!")
        access_token = token_info['access_token']
    else:
        url = request.url
        code = sp_oauth.parse_response_code(url)
        if code:
            print ("Found Spotify auth code in Request URL! Trying to get valid access token...")
            token_info = sp_oauth.get_access_token(code)
            access_token = token_info['access_token']

    if access_token:
        print ("Access token available! Trying to get user information...", access_token)
        sp = spotipy.Spotify(access_token)
        results = sp.current_user()
        print (results)
        return results

    else:
        return htmlLoginButton()

@route('/current-playing', method='GET')
def current_playing():
    access_token = ""

    token_info = sp_oauth.get_cached_token()
    if token_info:
        print ("Found cached token!")
        access_token = token_info['access_token']
    url = 'https://api.spotify.com/v1/me/player/currently-playing'
    headers = {'Authorization': 'Bearer ' + access_token, 'Accept': 'application/json', 'Content-Type': 'application/json'}

    try:
        response = requests.get(url, headers=headers)    
        data = response.json()
        return response.json()
    except:
        return "not existing current playing track!"


@route('/user-top-artists', method='GET')
def user_top_artists():
    access_token = ""

    token_info = sp_oauth.get_cached_token()
    if token_info:
        print ("Found cached token!")
        access_token = token_info['access_token']
    url = 'https://api.spotify.com/v1/me/top/artists'
    headers = {'Authorization': 'Bearer ' + access_token, 'Accept': 'application/json', 'Content-Type': 'application/json'}

    try:
        response = requests.get(url, headers=headers)
        print(response.json())
        return response.json()

    except:
        return "not existing user top artists!"


@route('/previous-track', method='POST')
def previous_track():
    access_token = ""

    token_info = sp_oauth.get_cached_token()
    if token_info:
        print ("Found cached token!")
        access_token = token_info['access_token']

    url = 'https://api.spotify.com/v1/me/player/previous'
    headers = {'Authorization': 'Bearer ' + access_token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
    params = {"device_id": "0d1841b0976bae2a3a310dd74c0f3df354899bc8"}
    try:
        response = requests.post(url, params = params, headers = headers)
        print(response.json())
        return response.json()
    except:
        print("can't move on previous track!")
        return "can't move on previus track!"

@route('/recently-played', method='GET')
def recently_played():
    access_token = ""

    token_info = sp_oauth.get_cached_token()
    if token_info:
        print ("Found cached token!")
        access_token = token_info['access_token']

    url = 'https://api.spotify.com/v1/me/player/recently-played'
    headers = {'Authorization': 'Bearer ' + access_token, 'Accept': 'application/json', 'Content-Type': 'application/json'}

    try:
        response = requests.post(url, headers=headers)
        print(response.json())
        return response.json()
    except:
        print("not existing recently played list!")
        return "not existing recently played list!"


@route('/featured-playlists', method='GET')
def featured_playlists():
    access_token = ""

    token_info = sp_oauth.get_cached_token()
    if token_info:
        print ("Found cached token!")
        access_token = token_info['access_token']

    url = 'https://api.spotify.com/v1/browse/featured-playlists'
    headers = {'Authorization': 'Bearer ' + access_token, 'Accept': 'application/json', 'Content-Type': 'application/json'}

    try:
        response = requests.post(url, headers=headers)
        print(response.json())
        return response.json()
    except:
        print("not existing featured playlists!")
        return "not existing featured playlists!"


def htmlLoginButton():
    auth_url = getSPOauthURI()
    htmlLoginButton = "<a href='" + auth_url + "'>Login to Spotify</a>"
    return htmlLoginButton
def getSPOauthURI():
    auth_url = sp_oauth.get_authorize_url()
    return auth_url

run(host='localhost', port=port)
