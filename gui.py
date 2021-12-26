import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from tkinter import filedialog
from util import *
from os.path import join, exists
from os import getcwd, rename, mkdir, remove
from urllib.request import urlopen
from yt_dlp import YoutubeDL

class ScraperGUI(tk.Tk):
    # Create GUI, the self.* variables are publicly accessible and can be modified
    # by other scripts
    def __init__(self):
        super().__init__()
        #self.tk.call("source", "azure.tcl")
        #self.tk.call("set_theme", "light")

        self.start_dir = ""
        self.title("Ultrastar scraper")
        mainframe = ttk.Frame(self, padding=(3, 3, 12, 12))
        mainframe.grid(column=0, row=0)

        self.ultrastar_file = tk.Text(mainframe)
        self.ultrastar_file.grid(column=1, row=2, columnspan=3)

        self.youtube_url = tk.StringVar()
        youtube_url_entry = ttk.Entry(mainframe, textvariable=self.youtube_url)
        youtube_url_entry.grid(column=2, row=3)

        self.cover_url = tk.StringVar()
        cover_url_entry = ttk.Entry(mainframe, textvariable=self.cover_url)
        cover_url_entry.grid(column=2, row=4)

        self.root_dir = tk.StringVar()
        root_dir_entry = ttk.Entry(mainframe, textvariable=self.root_dir)
        root_dir_entry.grid(column=2, row=5)

        ttk.Label(mainframe, text="Ultrastar File:").grid(row=1, column=1)
        ttk.Label(mainframe, text="Youtube URL:").grid(column=1, row=3)
        ttk.Label(mainframe, text="Cover Art URL:").grid(column=1, row=4)
        ttk.Label(mainframe, text="Root directory:").grid(column=1, row=5)
        ttk.Button(mainframe, text='Browse', command=lambda: self.choose_root_dir(self.start_dir)).grid(
            column=3, row=5, padx=3 )
        ttk.Button(mainframe, text='Scrape!',
                   command=self.scrape).grid(column=2, row=6, pady=3)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        mainframe.columnconfigure(0, weight=1)
        mainframe.columnconfigure(1, weight=1)
        mainframe.columnconfigure(2, weight=1)
        mainframe.rowconfigure(0, weight=1)
        mainframe.rowconfigure(1, weight=1)
        mainframe.rowconfigure(2, weight=1)

    def scrape(self):
        self.progress_window = ProgressBar()
        config_file = self.ultrastar_file.get("1.0", "end").split("\n")
        configuration = parse_ultrastar(config_file)
        if (check_ultrastar(configuration) < 0):
            messagebox.showerror(
                title="Error", message="Ultrastar file metadata could not be parsed")
            self.progress_window.destroy()
            return

        if (not exists(self.root_dir.get())):
            messagebox.showerror(
                title="Error", message="Root directory does not exists, check parameters and try again")
            self.progress_window.destroy()
            return
        song_dir = join(self.root_dir.get(),
                        configuration["ARTIST"] + " - " + configuration["TITLE"])
        allowed = True

        try:
            mkdir(song_dir)
        except FileExistsError:
            allowed = messagebox.askokcancel(title='Confirmation',
                                             message='Pressing OK will overwrite existing data',
                                             icon="warning")
        if (allowed):
            ultrastar_file_path = join(
                song_dir, configuration["ARTIST"] + " - " + configuration["TITLE"] + ".txt")
            with open(ultrastar_file_path, "w") as f:
                f.write(self.ultrastar_file.get("1.0", "end"))
            fail_song = self.download_song(
                self.youtube_url.get(), configuration, song_dir)
            if (fail_song):
                messagebox.showerror(
                    title="Error", message="Error song could not be downloaded, check Youtube URL")
                self.progress_window.destroy()
                return
            fail_cover = self.download_cover(
                self.cover_url.get(), configuration, song_dir)
            self.progress_window.destroy()
            
            if (fail_cover):
                messagebox.showwarning(
                    title="Warning", message="Error while downloading cover art, however song will still work")
            else:
                self.ultrastar_file.delete('1.0', "end")
                self.youtube_url.set('')
                self.cover_url.set('')
                messagebox.showinfo(
                    title="Success", message="Song downloaded successfully")

    def choose_root_dir(self, start_dir):
        if (start_dir == ""):
            start_dir = getcwd()
        filename = filedialog.askdirectory(initialdir=start_dir,
                                           title="Select a Directory")

        # Change label contents
        self.root_dir.set(0, filename)
    # Methods that downloads song from specified directory
    # static since it does not need the object

    def myhook(self, d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')
        if d['status'] == 'downloading':
            percent = int(float(d['_percent_str'][:-1]))
            self.progress_window.step(percent)
            self.update()


    def download_song(self, url, configuration, root_dir):
        keep_video = False
        mp3_filename = remove_suffix(configuration['MP3'], ".mp3")
        if ("VIDEO" in configuration):
            keep_video = True

        ydl_opts = {
            'format': 'best[ext=mp4][height<=720]',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': MyLogger(),
            'progress_hooks': [self.myhook],
            'outtmpl': join(root_dir, mp3_filename + '.%(ext)s'),
            'keepvideo': keep_video
        }

        with YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
            except:
                return -1

        if (keep_video):
            old_name = join(root_dir, mp3_filename + ".mp4")
            new_name = join(root_dir, configuration["VIDEO"])
            rename(old_name, new_name)
        return 0

    @staticmethod
    def download_cover(cover_url, configuration, root_dir):
        try:
            with urlopen(cover_url) as response:
                data = response.read()
                open(root_dir + "/" + configuration["COVER"], 'wb').write(data)
            return 0
        except:
            return -1


class ProgressBar(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.start_dir = ""
        self.title("Progress")
        self.pb = ttk.Progressbar(
            self,
            orient='horizontal',
            mode='determinate',
            length=280
        )
        # place the progressbar
        self.pb.grid(column=0, row=0, columnspan=2, padx=10, pady=20)

        # label
        self.value_label = ttk.Label(self, text="")
        self.value_label.grid(column=0, row=1, columnspan=2)
    def step(self, value):
        self.pb['value'] = value
        self.update_progress_label()
        self.update_idletasks()
    def update_progress_label(self):
        if (self.pb['value'] < 10):
            self.value_label.config(text="Initializing directory...")
        elif (self.pb['value'] < 80):
            self.value_label.config(text="Downloading song using youtube-dl")
        elif (self.pb['value'] < 100):
            self.value_label.config(text="Downloading cover art")
