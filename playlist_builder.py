import os
import random
from plexapi.server import PlexServer
from plexapi import exceptions as plexapi_exceptions
import configparser
from datetime import date

# Read configuration from the INI file
plex_config = configparser.ConfigParser()
plex_config.read("plex_config.ini")

# Get Plex server information from the configuration
baseurl = plex_config.get('PLEX_SERVER', 'baseurl')
token = plex_config.get('PLEX_SERVER', 'token')

# Plex server connection
plex = PlexServer(baseurl, token)
TODAY = date.today()

# Loop through each section in the INI file
for section_name in plex_config.sections():
    if section_name == 'PLEX_SERVER':
        continue  # Skip the PLEX_SERVER section

    # Get configuration values for the current section
    library_name = plex_config.get(section_name, 'library')
    rerun_flag = plex_config.get(section_name, 'rerun')
    episode_count = int(plex_config.get(section_name, 'episode_count'))
    shows_to_add = plex_config.get(section_name, 'shows')
    playlist_name = section_name  # Customize playlist name if needed
    type = plex_config.get(section_name, 'type')

    # Handle the case when 'excludedays' is not present in the configuration
    excludedays = plex_config.get(section_name, 'excludedays', fallback=None)
    if excludedays is not None:
        excludedays = int(excludedays)

    # Delete the playlist if it already exists
    for playlist in plex.playlists():
        if playlist.title == playlist_name:
            print('{} already exists. Deleting and rebuilding.'.format(playlist_name))
            playlist.delete()

    # List to store episodes for the playlist
    old_episodes_playlist = []

    if rerun_flag == "yes":
        if type == 'shows':
            # Processing shows for reruns
            tv_shows = shows_to_add.split(',')
            for show in tv_shows:
                NumberOfEpAlreadyAdded = 0
                plex_current_show = plex.library.section(library_name).get(show)
                for episode in plex_current_show.episodes():
                    if episode.lastViewedAt:
                        days_since_played = (TODAY - episode.lastViewedAt.date()).days
                        if days_since_played > excludedays:
                            old_episodes_playlist.append(episode)

        elif type == 'collections':
            # Processing collections for reruns
            collection_name = plex_config.get(section_name, 'shows')
        
            # Code for 'collections' type
            plex_collection = plex.library.section(library_name).collection(collection_name)
            for item in plex_collection.items():
                tv_show_name = item.title
                plex_current_show = plex.library.section(library_name).get(tv_show_name)
                for episode in plex_current_show.episodes():
                    if episode.lastViewedAt:
                        if episode.lastViewedAt:
                            days_since_played = (TODAY - episode.lastViewedAt.date()).days
                            if days_since_played > excludedays:
                                old_episodes_playlist.append(episode)
    elif rerun_flag =="no":
        if type == 'shows':
            # Processing shows for not reruns
            tv_shows = shows_to_add.split(',')
            for show in tv_shows:
                try:
                    plex_current_show = plex.library.section(library_name).get(show)
                except plexapi.exceptions.NotFound:
                    print(f"Unable to find item with title: {show}")

                # Find the last watched episode
                last_watched_episode = None
                for episode in plex_current_show.episodes():
                    if episode.lastViewedAt:
                        last_watched_episode = episode
                
                # Find the next unwatched episode after the last watched episode
                if last_watched_episode:
                    for episode in plex_current_show.episodes():
                        if episode.index > last_watched_episode.index and not episode.isPlayed:
                            old_episodes_playlist.append(episode)
                            break
                else:
                    # If there are no watched episodes, add the first unwatched episode
                    for episode in plex_current_show.episodes():
                        if not episode.isPlayed:
                            old_episodes_playlist.append(episode)
                            break
        elif type == 'collections':
            # Processing collections for not reruns
            collections = shows_to_add.split(',')
            
            for collection_name in collections:
                try:
                    plex_current_collection = plex.library.section(library_name).collection(collection_name)
                except plexapi_exceptions.NotFound:
                    print(f"Unable to find collection with title: {collection_name}")
                    continue  # Skip to the next collection if the current one is not found

                # Find the last watched episode in the collection
                last_watched_episode = None
                for item in plex_current_collection.items():
                    for episode in item.episodes():
                        if episode.lastViewedAt:
                            last_watched_episode = episode
                            break  # Exit the loop after finding the last watched episode
                    if last_watched_episode:
                        break  # Exit the outer loop if the last watched episode is found

                # Find the next unwatched episode after the last watched episode
                if last_watched_episode:
                    for item in plex_current_collection.items():
                        for episode in item.episodes():
                            if episode.index > last_watched_episode.index and not episode.isPlayed:
                                old_episodes_playlist.append(episode)
                                break  # Exit the loop after adding the first unwatched episode
                else:
                    # If there are no watched episodes, add the first unwatched episode in the collection
                    for item in plex_current_collection.items():
                        for episode in item.episodes():
                            if not episode.isPlayed:
                                old_episodes_playlist.append(episode)
                                break  # Exit the loop after adding the first unwatched episode

    # Shuffle the playlist
    random.shuffle(old_episodes_playlist)

    playlist_length = len(old_episodes_playlist)

    # Create the playlist
    if playlist_length > 0:
        final_playlist = old_episodes_playlist[:episode_count]
        print('Adding {} shows to playlist "{}".'.format(len(final_playlist), playlist_name))
        plex.createPlaylist(playlist_name, items=final_playlist)
    else:
        print('No episodes to add to playlist "{}".'.format(playlist_name))
