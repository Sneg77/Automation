
import spotipy
import spotipy.util as util
import time
import alsaaudio


spotifyUsername = ""
spotifyAccessScope = "user-library-read user-read-currently-playing user-read-playback-state,user-modify-playback-state"
spotifyClientId = ""
spotifyClientSecret = ""
spotifyRedirectURI = "https://www.google.com/"


def setupSpotify(username, scope, clientID, clientSecret, redirectURI):
    token = util.prompt_for_user_token(username, scope, clientID, clientSecret, redirectURI)
    return spotipy.Spotify(auth=token)


def volume(vol):
    mix = alsaaudio.Mixer() 
    mix.setvolume(vol)


def MuteSpotify(mute):
    if mute:
        volume(0)
    else:
        volume(100)


def main():
    global spotifyObject

    try:
        trackInfo = spotifyObject.current_user_playing_track()
    except:
        print("Token Expired")
        spotifyObject = setupSpotify(spotifyUsername, spotifyAccessScope, spotifyClientId, spotifyClientSecret, spotifyRedirectURI)
        trackInfo = spotifyObject.current_user_playing_track()
        print('its ok')
    try:
        if trackInfo['currently_playing_type'] == 'ad':
            MuteSpotify(True)
        else:
            MuteSpotify(False)
    except TypeError:
        pass


if __name__ == "__main__":
    spotifyObject = setupSpotify(spotifyUsername, spotifyAccessScope, spotifyClientId, spotifyClientSecret, spotifyRedirectURI)


while True:
    main()
    time.sleep(0.1)
