
class Music():
    def __init__(self, category, name, title, url, duration):
        self.category = category
        self.name = name
        self.title = title
        self.url = url
        self.duration = duration
    
    def __repr__(self):
        return f"{self.category}: {self.name} - {self.title}"
