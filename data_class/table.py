import os
from ytdl_utils.ytdl import fetch_data
from data_class.music import Music

class MusicTable():
    def __init__(self, txt):
        self.table = {}
        self.file = txt

        if not os.path.exists(self.file):
            f = open(self.file, 'w')
            f.close()
        
        self.load_music_info()

    def load_music_info(self):
        with open(self.file, 'r', encoding="utf-8") as f:
            for line in f:
                category, name, title, url = line.strip().split(",")
                self.table[name] = Music(category, name, title, url)

    def save_music_info(self):
        with open(self.file, 'w', encoding="utf-8") as f:
            for name in self.table:
                music = self.table[name]
                f.write(f"{music.category},{music.name},{music.title},{music.url}\n")
    

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
        self.table[name] = Music(category, name, data["title"], url)
        self.save_music_info()
        return True, f"{name}: {data['title']} has been added"

    def remove_music(self, name):
        """
        Remove name from music table, return true, msg on success false, err on fail
        """
        if name not in self.table:
            return False, f"The name {name} does not exist in the music table"

        self.table.pop(name)
        return True, f"{name} has been removed from the table"
    
    def get_url(self, name):
        """
        Return the url of vid by name
        """
        music = self.table.get(name, None)
        if music is None:
            return None
        return music.url 
    
    def get(self, name):
        return self.table.get(name, None)
    
    def get_paginated_category(self):
        music_by_category = {}

        # Map music by category
        for name in self.table:
            category = self.table[name].category
            if category not in music_by_category:
                music_by_category[category] = []
            
            music_by_category[category].append(self.table[name])
        
        return music_by_category

    def __repr__(self):
        """
        Repr of self
        """
        s = "Music Table: \n"
        music_by_category = self.get_paginated_category()
        
        # Create String repr
        for category in music_by_category:
            s += f"==={category}===\n"
            for music in music_by_category[category]:
                s += f"    {music.name}: {music.title}\n"
        
        s += "\n"
        return s


class SoundEffectTable():

    def __init__(self, txt):
        self.table = {}
        self.file = txt

        if not os.path.exists(self.file):
            f = open(self.file, 'w')
            f.close()
        
        self.load_sound_effect_info()

    def load_sound_effect_info(self):
        with open(self.file, 'r', encoding="utf-8") as f:
            for line in f:
                name, url = line.strip().split(",")
                self.table[name] = url

    def save_sound_effect_info(self):
        with open(self.file, 'w', encoding="utf-8") as f:
            keys = sorted(self.table.keys())
            for name in keys:
                url = self.table.get(name, "")
                f.write("{},{}\n".format(name, url))
    

    def add_sound_effect(self, name, url):
        """
        Add sound effect to table, return true, msg on success and false, error message on fail
        """
        name, url = name.strip(), url.strip()
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
        self.table[name] = url
        self.save_sound_effect_info()
        return True, f"Sound effect {name} has been added"

    def remove_sound_effect(self, name):
        """
        Remove name from sound_effect table, return true, msg on success false, err on fail
        """
        if name not in self.table:
            return False, f"The name {name} does not exist in the sound effect table"

        self.table.pop(name)
        return True, f"{name} has been removed from the table"
    
    def get_url(self, name):
        """
        Return the url of vid by name
        """
        return self.table.get(name, None)
    
    def __repr__(self):
        """
        Repr of self
        """
        s = "Sound Effect Table: \n"
        for name in self.table:
            s += f"    {name}\n"
            
        s += "\n"
        return s

if __name__ == "__main__":
    t = SoundEffectTable('./sound_effect.txt')
    print(t)