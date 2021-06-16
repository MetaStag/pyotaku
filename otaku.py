# pyotaku

# MODULES
from jikanpy import Jikan # Jikan API wrapper
from requests import get # To download images
from os import system, path # To clear screen and check for temp.jpg
import platform # To determine operating system

jikan = Jikan() # Initializing the Jikan instance

if platform.system() == "Darwin":
    image_viewing_command = 'open temp.jpg'
elif platform.system() == "Linux":
    image_viewing_command = 'xdg-open temp.jpg'
elif platform.system() == "Windows":
    image_viewing_command = 'start temp.jpg'
else:
    image_viewing_command = 'echo Sorry, we could not determine your platform, try setting an image viewing command manually'

# overwrite the image viewing command by changing and uncommenting the line below:
#image_viewing_command = "yourcommand temp.jpg"

# FUNCTIONS
# Search for anime/manga/character
def search():
    # Getting type of search (anime/manga/character)
    search_type = input('Select type -> (A)nime/(M)anga/(C)haracter: ')
    search_type = search_type.lower()

    if search_type in ['a', 'anime']:
        search_type = 'anime'
    elif search_type in ['m', 'manga']:
        search_type = 'manga'
    elif search_type in ['c', 'character']:
        search_type = 'character'
    else:
        print('Invalid input, write either a, m or c...')
        return False, False

    # Searching query
    query = input('Enter search query: ')
    search_results = jikan.search(search_type, query)

    if search_results == {}: # While MAL returns some sort of results no matter what the search query is, this check is there just in case
        print('No results were found...')
        return False, False

    return search_type, search_results

# Show search results in a somewhat clean way
def show_search_results(search_type, search_results):
    first = 'title'
    second = 'score'
    if search_type == 'anime':
        third = 'episodes'
    elif search_type == 'manga':
        third = 'chapters'
    elif search_type == 'character':
        first = 'name'
        second = 'alternative_names'
        third = 'anime/manga'

    
    print(f'NO.|    {first.upper()}    |    {second.upper()}    |    {third.upper()}    |    TYPE    |')
    print_seperator()

    num = 1
    if search_type == 'character': # Seperate loop for Character because it has different variables (anime/manga)
        for i in search_results["results"]:
            if len(i["anime"]) != 0:
                content_type = 'anime'
            else:
                content_type = 'manga'

            # following block determines anime or manga with lowest mal_id
            # to show the oldest anime that a character appeared in
            animelist = []
            for number in i[content_type]:
                pass
                animelist.append(number["mal_id"])

            titleindex = animelist.index(min(sorted(animelist)))
            # below line prints a number, the character name, nicknames, the anime/manga name, whether or not its an anime or manga
            print(f'|{num}| {i[first]} | {i[second]} | {i[content_type][titleindex][first]} | {i[content_type][0]["type"]}')
            num += 1
            if num == 11: # Limit of 10 results
                break
        print_seperator()
        return

    for i in search_results["results"]:
        print(f'|{num}| {i[first]} | {i[second]} | {i[third]} | {i["type"]}')
        num += 1
        if num == 11: # Limit of 10 results
            break
    print_seperator()

# Check info on a specific anime/manga/character
def check_info(search_type, query):

    # Print info
    if search_type == 'anime':
        anime = jikan.anime(query['mal_id'])
        print(f'Title      | {anime["title"]}')
        print(f'Title(en)  |  {anime["title_english"]}')
        print(f'Type       | {anime["type"]}')
        print(f'Episodes   | {anime["episodes"]}')
        print_seperator(45)
        print(f'Rank       | {anime["rank"]}')
        print(f'Popularity | {anime["popularity"]}')
        print(f'Score      | {anime["score"]}')
        print(f'Members    | {anime["members"]}')
        print_seperator(45)
        print(f'Airing     | {anime["airing"]}')
        print(f'Aired      | {anime["aired"]["string"]}')
        print_seperator(45)
        print(f'Synopsis   | {anime["synopsis"][:-25]}')
        print_seperator(45)
        print(f'Url        | {anime["url"]}')
        print_seperator(45)

    elif search_type == 'manga':
        manga = jikan.manga(query['mal_id'])
        print(f'Title      | {manga["title"]}')
        print(f'Volumes    | {manga["volumes"]}')
        print(f'Chapter    | {manga["chapters"]}')
        print_seperator(45)
        print(f'Rank       | {manga["rank"]}')
        print(f'Popularity | {manga["popularity"]}')
        print(f'Score      | {manga["score"]}')
        print(f'Members    | {manga["members"]}')
        print_seperator(45)
        print(f'Published  | {manga["published"]["string"]}')
        print(f'Status     | {manga["status"]}')
        print_seperator(45)
        print(f'Sypnosis   | {manga["synopsis"][:-25]}')
        print_seperator(45)
        print(f'Url        | {manga["url"]}')
        print_seperator(45)

    elif search_type == 'character':
        character = jikan.character(query['mal_id'])
        print(f'Name             | {character["name"]}')
        if len(character["animeography"]) > 0:
            print(f'Animeography     | {character["animeography"][0]["name"]}')
        else:
            print("Animeography     | None")
        if len(character["mangaography"]) > 0:
            print(f'Mangaography     | {character["mangaography"][0]["name"]}')
        else:
            print("Mangaography     | None")
        print_seperator(45)
        print(f'Nicknames        | {character["nicknames"]}')
        print_seperator(45)
        print(f'Member Favorites | {character["member_favorites"]}')
        print_seperator(45)
        print(f'About            | {character["about"]}')
        print_seperator(45)
        print(f'Url              | {character["url"]}')
        print_seperator(45)

    
    # Corresponding Image
    choice = input('Do you want to open the corresponding image(y/N): ')
    choice = choice.lower()

    if choice in ['y', 'yes']:
        img_url = query["image_url"]
        response = get(query["image_url"], stream=True) # Download Image
        with open('temp.jpg', 'wb') as file: # Save to external file temporarily
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        system(image_viewing_command) # Display Image

# Clear the screen
def clear():
    system('clear')
    print('pyotaku')
    print('*' * 7)
    print('COMMANDS')
    print('s - Search')
    print('c - Check info')
    print('a - Add a title to list')
    print('d - Delete a title from list')
    print('l - List saved titles')
    print('clear - Clear the Screen')
    print('q - Exit')
    print('*' * 7)

def print_seperator(length=63):
    print("_" * length)


# MAIN LOOP
if __name__ == "__main__":
    clear()
    while True:
        choice = input('> ').lower()

        if choice == 's': # Search
            search_type, search_results = search()

            if not search_type: # If search_type was invalid or search returned no results
                continue
            show_search_results(search_type, search_results)

        elif choice == 'c': # Check info
            search_type, search_results = search()

            if not search_type:
                continue
            check_info(search_type, search_results['results'][0])

        elif choice == 'a': # Add a title to list
            title = input('Enter name of title: ')
            with open('list.txt', 'a') as f:
                f.write(f'{title}\n')
            print('Sucessfully added title to list!')

        elif choice == 'd': # Delete a title from list
            title = input('Enter name of title: ')
            flag = False
            with open('list.txt', 'r+') as f:
                titles = f.readlines()
                f.seek(0)
                for i in titles:
                    if i == f'{title}\n':
                        flag = True
                    else:
                        f.write(i)
                f.truncate()

            if flag:
                print('Sucessfully deleted title from list!')
            else:
                print('This title does not exist...')

        elif choice == 'l': # List all titles
            try:
                with open('list.txt', 'r') as f:
                    titles = f.readlines()
            except:
                print("The list file doesn't exist! Sorry!")

            if titles == []:
                print('The list is currently empty...')
                continue
            for i in titles:
                print(f'{titles.index(i)+1}: {i[:-1]}')

        elif choice == 'clear': # Clear the Screen
            clear()

        elif choice in ['q', 'exit']:
            if platform.system == "Windows":
                if path.exists("temp.jpg"):
                    system("del temp.jpg")
            else:
                system("rm -f temp.jpg")
            exit()

        else:
            print('Invalid Command...')
