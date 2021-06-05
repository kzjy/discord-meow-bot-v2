import youtube_dl
import discord
from data_class.music import Music

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': False,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

def fetch_data(url):
    """
    Get data of video by url, return none if err
    return 
        Success: data
        Error: None
    """
    try:
        info = ytdl.extract_info(url, download=False)
        return info
    except Exception:
        return None

def fetch_audio_source(url):
    """
    Get audio source
    return 
        Success: AudioSource
        Error: None
    """
    info = fetch_data(url)
    if info is None:
        return None

    URL = info['formats'][0]['url']
    return discord.FFmpegPCMAudio(URL, executable="./ffmpeg.exe", **FFMPEG_OPTIONS)