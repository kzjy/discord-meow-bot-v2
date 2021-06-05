from data_class.music import Music
from data_class.table import *
from ytdl_utils.ytdl import fetch_data

# new_table = MusicTable("./new_music.txt")

# with open("./music.txt", "r", encoding="utf-8") as rf:
#     for line in rf:
#         category, name, title, url = line.strip().split(",")
#         data = fetch_data(url)
#         duration = data['duration']

#         new_table.add_music(category, name, url)
            
new_table = SoundEffectTable("./new_sound.txt")

with open("./sound_effect.txt", "r", encoding="utf-8") as rf:
    for line in rf:
        name, url = line.strip().split(",")

        new_table.add_sound_effect("misc", name, url)