import os
from ytdl_utils.ytdl import fetch_data
from data_class.music import Music

class Table():
    def __init__(self, txt):
        self.table = {}
        self.file = txt

        if not os.path.exists(self.file):
            f = open(self.file, 'w')
            f.close()
        
        self.load_table()

    def load_table(self):
        with open(self.file, 'r', encoding="utf-8") as f:
            for line in f:
                category, name, title, url, duration = line.strip().split(",")
                self.table[name] = Music(category, name, title, url, int(duration))

    def save_table(self):
        with open(self.file, 'w', encoding="utf-8") as f:
            for name in self.table:
                music = self.table[name]
                f.write(f"{music.category},{music.name},{music.title},{music.url},{music.duration}\n")
    
    def get_url(self, name):
        """
        Return the url of vid by name
        """
        music = self.table.get(name, None)
        if music is None:
            return None
        return music.url 
    
    def get_paginated_category(self):
        music_by_category = {}

        # Map music by category
        for name in self.table:
            category = self.table[name].category
            if category not in music_by_category:
                music_by_category[category] = []
            
            music_by_category[category].append(self.table[name])
        
        return music_by_category
    
    def get(self, name):
        return self.table.get(name, None)


class MusicTable(Table):

    def __init__(self, txt):
        super(MusicTable, self).__init__(txt)
    

    def add_music(self, category, name, url):
        """
        Add music to music table, return true, msg on success and false, error message on fail
        """
        name, category, url = name.strip(), category.strip(), url.strip()

        if name in self.table:
            return False, "The id {} already exists in the table".format(name)

        data = fetch_data(url)

        # Failed to get video data
        if data is None:
            return False, "The video is unavailable"
        
        
        # Add to table
        self.table[name] = Music(category, name, data["title"], url, int(data['duration']))
        self.save_table()
        return True, f"{name}: {data['title']} has been added"

    def remove_music(self, name):
        """
        Remove name from music table, return true, msg on success false, err on fail
        """
        if name not in self.table:
            return False, f"The name {name} does not exist in the music table"

        self.table.pop(name)
        return True, f"{name} has been removed from the table"
    

class SoundEffectTable(Table):

    def __init__(self, txt):
        super(SoundEffectTable, self).__init__(txt)
    

    def add_sound_effect(self, category, name, url):
        """
        Add sound effect to table, return true, msg on success and false, error message on fail
        """
        category, name, url = category.strip(), name.strip(), url.strip()
        if name in self.table:
            return False, f"The id {name} already exists in the table"

        data = fetch_data(url)

        # Video unavailable
        if data is None:
            return False, "The sound effect is unavailable"
        
        # Video too long for sound effect
        if data['duration'] > 30:
            return False, "Sound effects should be < 30 seconds!"

        # Add to table
        self.table[name] = Music(category, name, data["title"], url, int(data['duration']))
        self.save_table()
        return True, f"Sound effect {name} has been added"

    def remove_sound_effect(self, name):
        """
        Remove name from sound_effect table, return true, msg on success false, err on fail
        """
        if name not in self.table:
            return False, f"The name {name} does not exist in the sound effect table"

        self.table.pop(name)
        return True, f"{name} has been removed from the table"
    

if __name__ == "__main__":
    t = SoundEffectTable('./sound_effect.txt')
    print(t)