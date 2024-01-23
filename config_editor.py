import os
import configparser
import questionary
from plexapi.server import PlexServer
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def display_menu():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
    print_color_box("Main Menu", Fore.YELLOW + Style.BRIGHT)
    choice = questionary.select("Choose an option:", choices=["Create a Playlist","Playlist refresh schedule","Edit Plex Server Settings","Exit"]).ask()
    return choice

def display_server_info(config):
    if 'PLEX_SERVER' in config and 'baseurl' in config['PLEX_SERVER'] and 'token' in config['PLEX_SERVER']:
        server_url = config['PLEX_SERVER']['baseurl']
        token = config['PLEX_SERVER']['token']
        print(f"\n{Fore.CYAN}Connected to Plex Server:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}URL:{Style.RESET_ALL} {server_url}")
        print(f"  {Fore.GREEN}Token:{Style.RESET_ALL} {token}\n")

def display_playlist_count(config):
    playlist_count = len([section for section in config.sections() if section != 'PLEX_SERVER'])
    print(f"{Fore.MAGENTA}Number of Playlists:{Style.RESET_ALL} {playlist_count}\n")

def print_color_box(message, color=Fore.WHITE + Style.BRIGHT):
    width = len(message) + 4
    print(color + "+" + "-" * width + "+")
    print("| " + message + " |")
    print("+" + "-" * width + "+" + Style.RESET_ALL)

def create_plex_config():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
    config = configparser.ConfigParser()
    config.read('plex_config.ini')

    display_server_info(config)
    display_playlist_count(config)

    # Check if baseurl and token are present in the configuration file
    if 'PLEX_SERVER' not in config or 'baseurl' not in config['PLEX_SERVER'] or 'token' not in config['PLEX_SERVER']:
        print_color_box("Plex Server Configuration", Fore.YELLOW + Style.BRIGHT)
        baseurl = input("Enter the URL of your Plex server: ")
        token = input("Enter the token of your Plex server: ")

        # Save baseurl and token to the configuration file
        config['PLEX_SERVER'] = {
            'baseurl': baseurl,
            'token': token,
        }

        with open('plex_config.ini', 'w') as configfile:
            config.write(configfile)

        print(f"\n{Fore.GREEN}Plex server configuration saved successfully.{Style.RESET_ALL}")
    else:
        print("Plex server configuration found in plex_config.ini.")

    print_color_box("Create a Playlist Configuration", Fore.YELLOW + Style.BRIGHT)

    # Ask for playlist name
    playlist_name = input("Enter the name of the Plex playlist: ")

    # Create a new section for the playlist
    config[playlist_name] = {}

    # Get Plex server instance
    baseurl = config['PLEX_SERVER']['baseurl']
    token = config['PLEX_SERVER']['token']
    plex = PlexServer(baseurl, token)

    # Ask for playlist type (shows or collections)
    playlist_type = questionary.select("Choose playlist type:", choices=["Shows", "Collections"]).ask()

    # Display and select library name
    libraries = plex.library.sections()
    print(f"\n{Fore.CYAN}Available Libraries:{Style.RESET_ALL}")
    selected_library = questionary.select("Choose a library:", choices=[library.title for library in libraries]).ask()
    config[playlist_name]['library'] = selected_library

    # Ask if it's for New Episodes or Reruns
    rerun_answer = questionary.confirm("Is this playlist for reruns?").ask()
    playlist_section = config[playlist_name]
    playlist_section['rerun'] = "yes" if rerun_answer else "no"

    # Ask how many episodes should be in the playlist
    episode_count = questionary.text("Enter the number of episodes for the playlist:").ask()
    playlist_section['episode_count'] = episode_count

    is_rerun = playlist_section['rerun'] == "yes"

    if is_rerun:
        # Ask how many days to exclude a played episode
        played_exclude_days = questionary.text("Enter the number of days to exclude a played episode:").ask()
        playlist_section['excludedays'] = played_exclude_days
         # Handle the case when it's not for reruns
        if playlist_type == "Shows":
            playlist_section['shows'] = ','.join(f'{show}' for show in get_plex_shows(plex, playlist_section))
            playlist_section['type'] = 'shows'
        elif playlist_type == "Collections":
            playlist_section['shows'] = ','.join(f'{collection}' for collection in get_plex_collections(plex, playlist_section))
            playlist_section['type'] = 'collections'
    else:
        # Handle the case when it's not for reruns
        if playlist_type == "Shows":
            playlist_section['shows'] = ','.join(f'{show}' for show in get_plex_shows(plex, playlist_section))
            playlist_section['type'] = 'shows'
        elif playlist_type == "Collections":
            playlist_section['shows'] = ','.join(f'{collection}' for collection in get_plex_collections(plex, playlist_section))
            playlist_section['type'] = 'collections'

    with open('plex_config.ini', 'w') as configfile:
        config.write(configfile)

    print_color_box(f"{Fore.GREEN}Playlist '{playlist_name}' configuration saved successfully.{Style.RESET_ALL}")
    display_playlist_count(config)

    input("\nPress Enter to return to the main menu")

def get_plex_shows(plex, playlist_section):
    selected_library = playlist_section.get('library', '')
    shows = [show.title for show in plex.library.section(selected_library).all()]

    questions = [
        {
            'type': 'checkbox',
            'message': f'Select TV shows from library "{selected_library}":',
            'name': 'selected_shows',
            'choices': [{'name': show} for show in shows],
        }
    ]

    answers = questionary.prompt(questions)
    selected_shows = answers.get('selected_shows', [])

    #playlist_section['shows'] = ','.join(f'"{show}"' for show in selected_shows)
    playlist_section['shows'] = ','.join(selected_shows)
    playlist_section['type'] = 'shows'

    return selected_shows

def get_plex_collections(plex, playlist_section):
    selected_library = playlist_section.get('library', '')
    collections = [collection.title for collection in plex.library.section(selected_library).collections()]

    questions = [
        {
            'type': 'checkbox',
            'message': f'Select collections from library "{selected_library}":',
            'name': 'selected_collections',
            'choices': [{'name': collection} for collection in collections],
        }
    ]

    answers = questionary.prompt(questions)
    selected_collections = answers.get('selected_collections', [])

    #playlist_section['shows'] = ','.join(f'"{collection}"' for collection in selected_collections)
    playlist_section['shows'] = ','.join(selected_collections)


    playlist_section['type'] = 'collections'

    return selected_collections

def edit_plex_settings():
    # Read the configuration file
    plex_config = configparser.ConfigParser()
    plex_config_file = "plex_config.ini"
    plex_config.read(plex_config_file)

    # Check if PLEX_SERVER section exists in the configuration
    if 'PLEX_SERVER' in plex_config:
        current_baseurl = plex_config.get('PLEX_SERVER', 'baseurl')
        current_token = plex_config.get('PLEX_SERVER', 'token')

        print(f"\nCurrent Plex Server Settings:")
        print(f"  {Fore.GREEN}Base URL:{Style.RESET_ALL} {current_baseurl}")
        print(f"  {Fore.GREEN}Token:{Style.RESET_ALL} {current_token}")

        # Ask if the user wants to edit the settings
        edit_settings = questionary.confirm("Do you want to edit these settings?").ask()

        if edit_settings:
            # Prompt the user for new values
            new_baseurl = questionary.text("Enter new base URL:", default=current_baseurl).ask()
            new_token = questionary.text("Enter new token:", default=current_token).ask()

            # Update the configuration
            plex_config.set('PLEX_SERVER', 'baseurl', new_baseurl)
            plex_config.set('PLEX_SERVER', 'token', new_token)

            with open(plex_config_file, 'w') as configfile:
                plex_config.write(configfile)

            print("Plex server settings updated.")
    else:
        print("Error: PLEX_SERVER section not found in the configuration file.")

def create_cron_file():
    #cron_file_path = questionary.text("Enter the path for the cron file:", default="plex_playlist_cron").ask()
    #cron_exists = os.path.exists(cron_file_path)

    cron_file_path = '/etc/cron.d/plex_playlist_cron'

    if os.path.exists(cron_file_path):
        print(f"The cron file '{cron_file_path}' exists.")
        cron_exists = os.path.exists(cron_file_path)
    else:
        print(f"The cron file '{cron_file_path}' does not exist.")

    if not cron_exists:
        print(f"Cron file not found. Creating a new cron file at {cron_file_path}.")
        # Create a new cron file
        with open(cron_file_path, 'w') as cronfile:
            pass

    schedule_type = questionary.select(
        "Select schedule type:",
        choices=["Daily", "Weekly"]
    ).ask()

    if schedule_type == "Daily":
        times_per_day = questionary.text("Enter the number of times per day:", default="1").ask()
        hours = questionary.text("Enter the hours (comma-separated):", default="4").ask()
        cron_expression = f"0 {hours} * * *"
    elif schedule_type == "Weekly":
        day_of_week = questionary.select(
            "Select the day of the week:",
            choices=["0 (Sunday)", "1 (Monday)", "2 (Tuesday)", "3 (Wednesday)", "4 (Thursday)", "5 (Friday)", "6 (Saturday)"]
        ).ask()
        hours = questionary.text("Enter the hours (comma-separated):", default="4").ask()
        cron_expression = f"0 {hours} * * {day_of_week}"

    # Overwrite the existing cron file
    with open(cron_file_path, 'w') as cronfile:
        cronfile.write(f"{cron_expression} /usr/src/app/entrypoint.sh\n")

    print(f"Cron schedule added to '{cron_file_path}'.")

if __name__ == "__main__":
    while True:
        choice = display_menu()

        if choice == "Create a Playlist":
            create_plex_config()
        elif choice == "Edit Plex Server Settings":
            edit_plex_settings()
        elif choice == "Playlist refresh schedule":
            create_cron_file()
        elif choice == "Exit":
            break
