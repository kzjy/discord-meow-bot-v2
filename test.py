from ytdl_utils.ytdl import fetch_data, ytdl, fetch_audio_source
from data_class.table import MusicTable

# msg = "~play fancy twice"
# print(msg.strip().split(" "))
# arg = msg.split(" ")[1:]
# arg = " ".join(arg)
# print(arg)
# data = ytdl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
# print(data.keys())
# # print(data['title'], data['webpage_url'])
# print(data['formats'][0])


from concurrent.futures import ThreadPoolExecutor
import threading
import time
import random

def task():
    print("Executing our Task")
    result = 0
    i = 0
    for i in range(10):
        result = result + i
    
    time.sleep(10)
    print("I: {}".format(result))
    print("Task Executed {}".format(threading.current_thread()))

def main():
    executor = ThreadPoolExecutor(max_workers=3)
    for i in range(20):
        task1 = executor.submit(task)

    
    return "finished"

if __name__ == '__main__':
    main()