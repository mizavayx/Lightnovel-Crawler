class Series:
    def __init__(self):
        self.Title = ""
        self.Translator = ""
        self.Group = ""
        self.Cover = ""
        self.Description = []
        self.BaseUrl = ""
        self.Id = ""
        self.Status = ""
        self.Author = ""
        self.Artist = ""
        self.Volumes = []


class Volume:
    def __init__(self):
        self.Title = ""
        self.Cover = ""
        self.Chapters = []


class Chapter:
    def __init__(self):
        self.Title = ""
        self.Url = ""
