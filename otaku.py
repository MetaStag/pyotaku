# pyotaku

# MODULES
from jikanpy import Jikan # Jikan API wrapper
from requests import get # To download images
from os import system # To clear screen
import platform

jikan = Jikan() # Initializing the Jikan instance

# Replace this with your command
if platform.system() == "Darwin":
    image_viewing_command = 'open temp.jpg'
elif platform.system() == "Linux":
    image_viewing_command = 'xdg-open temp.jpg'
elif platform.system() == "Windows":
    image_viewing_command = 'start temp.jpg'
else:
    image_viewing_command = ''

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
    if search_type == 'anime':
        first = 'title'
        second = 'score'
        third = 'episodes'
    elif search_type == 'manga':
        first = 'title'
        second = 'score'
        third = 'chapters'
    elif search_type == 'character':
        first = 'name'
        second = 'alternative_names'
        third = 'anime/manga'

    
    print(f'NO.|    {first.upper()}    |    {second.upper()}    |    {third.upper()}    |    TYPE    |')
    print('_______________________________________________________________')

    num = 1
    if search_type == 'character': # Seperate loop for Character because it has different variables (anime/manga)
        for i in search_results["results"]:
            if len(i["anime"]) != 0:
                content_type = 'anime'
            else:
                content_type = 'manga'

            print(f'|{num}| {i[first]} | {i[second]} | {i[content_type][0][first]} | {i[content_type][0]["type"]}')
            num += 1
            if num == 11: # Limit of 10 results
                break
        print('_______________________________________________________________')
        return

    for i in search_results["results"]:
        print(f'|{num}| {i[first]} | {i[second]} | {i[third]} | {i["type"]}')
        num += 1
        if num == 11: # Limit of 10 results
            break
    print('_______________________________________________________________')

# Check info on a specific anime/manga/character
def check_info(search_type, query):

    # Print info
    if search_type == 'anime':
        anime = jikan.anime(query['mal_id'])
        print(f'Title      | {anime["title"]}')
        print(f'Title(en)  |  {anime["title_english"]}')
        print(f'Type       | {anime["type"]}')
        print(f'Episodes   | {anime["episodes"]}')
        print('---------------------------------------------')
        print(f'Rank       | {anime["rank"]}')
        print(f'Popularity | {anime["popularity"]}')
        print(f'Score      | {anime["score"]}')
        print(f'Members    | {anime["members"]}')
        print('---------------------------------------------')
        print(f'Airing     | {anime["airing"]}')
        print(f'Aired      | {anime["aired"]["string"]}')
        print('---------------------------------------------')
        print(f'Synopsis   | {anime["synopsis"][:-25]}')
        print('---------------------------------------------')
        print(f'Url        | {anime["url"]}')
        print('---------------------------------------------')

    elif search_type == 'manga':
        manga = jikan.manga(query['mal_id'])
        print(f'Title      | {manga["title"]}')
        print(f'Volumes    | {manga["volumes"]}')
        print(f'Chapter    | {manga["chapters"]}')
        print('---------------------------------------------')
        print(f'Rank       | {manga["rank"]}')
        print(f'Popularity | {manga["popularity"]}')
        print(f'Score      | {manga["score"]}')
        print(f'Members    | {manga["members"]}')
        print('---------------------------------------------')
        print(f'Published  | {manga["published"]["string"]}')
        print(f'Status     | {manga["status"]}')
        print('---------------------------------------------')
        print(f'Sypnosis   | {manga["synopsis"][:-25]}')
        print('---------------------------------------------')
        print(f'Url        | {manga["url"]}')
        print('---------------------------------------------')

    elif search_type == 'character':
        character = jikan.character(query['mal_id'])
        print(f'Name             | {character["name"]}')
        print(f'Animeography     | {character["animeography"][0]["name"]}')
        print(f'Mangaography     | {character["mangaography"][0]["name"]}')
        print('---------------------------------------------')
        print(f'Nicknames        | {character["nicknames"]}')
        print(f'Member Favorites | {character["member_favorites"]}')
        print('---------------------------------------------')
        print(f'About            | {character["about"]}')
        print('---------------------------------------------')
        print(f'Url              | {character["url"]}')
        print('---------------------------------------------')

    
    # Corresponding Image
    while True:
        choice = input('Do you want to open the corresponding image(Y/N): ')
        choice = choice.lower()

        if choice == 'y':
            img_url = query["image_url"]
            response = get(query["image_url"], stream=True) # Download Image
            with open('temp.jpg', 'wb') as file: # Save to external file temporarily
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            system(image_viewing_command) # Display Image
            break
        elif choice == 'n':
            break
        else:
            print('Write either Y or N...')

# Clear the screen
def clear():
    system('clear')
    print('pyotaku')
    print('********')
    print('COMMANDS')
    print('s - Search')
    print('c - Check  info')
    print('a - Add a title to list')
    print('d - Delete a title from list')
    print('l - List saved titles')
    print('clear - Clear the Screen')
    print('q/exit - Exit')
    print('********')


# MAIN LOOP
clear()
while True:

    choice = input('> ')
    choice = choice.lower() # Managing case-sensitivity

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
        with open('list.txt', 'r') as f:
            titles = f.readlines()

        if titles == []:
            print('The list is currently empty...')
            continue
        for i in titles:
            print(f'{titles.index(i)+1}: {i[:-1]}')

    elif choice == 'clear': # Clear the Screen
        clear()
    elif choice in ['q', 'exit']:
        system("rm temp.jpg")
        exit()
    else:
        print('Invalid Command...')
