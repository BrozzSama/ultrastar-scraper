# Ultrastar Scraper

## Summary

This project aims at providing an easy interface to create ultrastar songs starting from a file and URLs for the associated Youtube video and cover art.

## How to use

If you are a user grab the latest release from the releases section on Github. Open the application and copy the content of the ultrastar file in the first block, the Youtube URL in the second, the cover art in the third and finally choose the destination directory (note that the directory will be automatically created in the format Title - Artist).

If you are a developer or have some degree of experience with Python you can clone this git repository with:

```
git clone https://github.com/BrozzSama/ultrastar-scraper
```

create a virtual environment inside the ultrastar-scraper directory and run into it with

```
python -m venv myvenv
source myvenv/bin/activate
```

grab the necessary dependencies with pip

```
pip -r requirements.txt
```

and finally run the Python script

```
python main.py
```

This will allow you to run the latest version straight from git.

## How to contribute

If you encounter an issue you're more than welcome to open an issue ticket on github or just send a PR fixing it, it is a relatively small project therefore no real "process" is needed.