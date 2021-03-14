# pyotaku

This python program allows you to search and check info on anime/manga and related characters... all from the terminal!

---
### Requirements
- Python
- jikanpy module (Jikan API wrapper)
    - use `pip install jikanpy` to install it

### Setup
This program only has one file, `otaku.py`, store it wherever you like.
The program will automatically create `list.txt` in the same folder to store the names of anime/manga you tell.

The program will also create a temporary file, `temp.jpg` in the same folder whenever you view an image.

The program by-default opens the images in `feh`. If you don't have that installed or want to use something else, open `otaku.py` and replace `image_viewing_command` with the command of your image viewer. For example, if you're using gwenview, you'll write `gwenview temp.jpg`.

### Usage 
- cd into the directory where `otaku.py` is located.
- run the program using `python otaku.py` (or `python3 otaku.py` if you have python 2.7 installed as well)

**Tip**-> As you have noticed, the process to launch this program is a bit tedious. what i would recommend is setting up an alias, here's an example:
```bash
# tested on bash and fish
alias anime='cd /path/to/file ; python otaku.py ; cd'
```

### Features

- Search for anime/manga/characters
- Check info on a particular anime/manga/characters
- Store names of anime/manga, etc. in a list
    - You might want to do this if you find an interesting anime, but don't have time to research on it so you save it here for later view.
    - You can delete the entries from the list as well. 

I initially wanted to add the functionality to read comments as well, but apparently Jikan API doesn't support that.

### License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/MetaStag/pyotaku/blob/main/LICENSE) file for details.
