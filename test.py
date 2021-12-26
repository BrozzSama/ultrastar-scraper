#!/usr/bin/python3
from gui import ScraperGUI

myWindow = ScraperGUI()
myWindow.ultrastar_file.insert("1.0", "#TITLE:Amare\n#ARTIST:La Rappresentante di Lista\n#YEAR:2021\n#MP3:amare.mp3\n#COVER:cover.jpg\n#VIDEO:amare.mp4\n#BPM:130\n#GAP:7220\n")
myWindow.youtube_url.set("https://youtu.be/iY9YsLvNNt8")
myWindow.cover_url.set("https://upload.wikimedia.org/wikipedia/en/0/0b/La_Rappresentante_di_Lista_-_Amare_-_Single_cover.jpg")
myWindow.root_dir.set("./")
myWindow.mainloop()

