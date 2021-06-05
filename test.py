from ytdl_utils.ytdl import fetch_data, ytdl, fetch_audio_source
from data_class.table import MusicTable

table = MusicTable("./music.txt")
# msg = "~play               "
# print(msg.strip().split(" "))
# # arg = msg.split(" ")[1:]
# # arg = " ".join(arg)
# # print(arg)
# # data = ytdl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
# # print(data['title'], data['webpage_url'])
print(table.get_paginated_keys())