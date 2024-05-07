from enum import Enum


class SourceTypes(Enum):
    SONG = "song"
    ALBUM = "album"
    ARTIST = "artist"
    LYRICS = "lyrics"


class SourcePages(Enum):
    YOUTUBE = "youtube", "https://www.youtube.com/"
    MUSIFY = "musify", "https://musify.club/"
    YOUTUBE_MUSIC = "youtube music", "https://music.youtube.com/"
    GENIUS = "genius", "https://genius.com/"
    MUSICBRAINZ = "musicbrainz", "https://musicbrainz.org/"
    ENCYCLOPAEDIA_METALLUM = "encyclopaedia metallum"
    BANDCAMP = "bandcamp", "https://bandcamp.com/"
    DEEZER = "deezer", "https://www.deezer.com/"
    SPOTIFY = "spotify", "https://open.spotify.com/"

    # This has nothing to do with audio, but bands can be here
    WIKIPEDIA = "wikipedia", "https://en.wikipedia.org/wiki/Main_Page"
    INSTAGRAM = "instagram", "https://www.instagram.com/"
    FACEBOOK = "facebook", "https://www.facebook.com/"
    TWITTER = "twitter", "https://twitter.com/"
    MYSPACE = "myspace", "https://myspace.com/"     # Yes somehow this ancient site is linked EVERYWHERE

    MANUAL = "manual", ""
    
    PRESET = "preset", ""

    def __new__(cls, value, homepage = None):
        member = object.__new__(cls)
    
        member._value_ = value
        member.homepage = homepage

        return member
        