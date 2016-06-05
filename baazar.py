appCategoryList = ["books-reference", "busines", "comics", "communication", "education", "entertainment",
                   "finance", "health-fitness", "libraries-demo", "lifestyle", "live-wallpaper", "media-video",
                   "medical", "music-audio", "news-magazines", "personalization", "photography", "productivity",
                   "religious", "shopping", "social", "sports", "tools", "transportation", "travel-local", "weather",
                   "widgets"]
gameCategoryList = ["action", "adventure", "arcade", "board", "casual", "educational", "family", "music", "puzzle",
                    "racing", "role-playing", "simulation", "sports", "strategy", "trivia", "word"]
'''

from enum import Enum
#use 'pip install enum34'

class Games(Enum):
    Action = "action"
    Adventure = "adventure"
    Arcade = "arcade"
    Board = "board"
    Casual = "casual"
    Educational = "educational"
    Family = "family"
    Music = "music"
    Puzzle = "puzzle"
    Racing = "racing"
    RolePlaying = "role-playing"
    Simulation = "simulation"
    Sports = "sports-game"
    Strategy = "strategy"
    Trivia = "trivia"
    Word = "word"

class APPS(Enum):
    Books = "books-reference"
    Business = "busines"
    Comics = "comics"
    Communication = "communication"
    Education = "education"
    Entertainment = "entertainment"
    Finance = "finance"
    Health = "health-fitness"
    Libraries = "libraries-demo"
    LifeStyle = "lifestyle"
    LiveWallpaper = "live-wallpaper"
    Media = "media-video"
    Medical = "medical"
    Music = "music-audio"
    News = "news-magazines"
    Personalization = "personalization"
    Photography = "photography"
    Productivity = "productivity"
    Religious = "religious"
    Shopping = "shopping"
    Social = "social"
    Sport = "sports"
    Tools = "tools"
    Transportation = "transportation"
    Travel = "travel-local"
    Weather = "weather"
    Widgets = "widgets"
 '''
