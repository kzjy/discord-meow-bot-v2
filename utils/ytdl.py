import youtube_dl
import discord
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

if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=rpBbgLgA0uZ"
    data = ytdl.extract_info(url, download=False)
    print(data, data['title'])