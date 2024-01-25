# PlexPlaylistHelper

PlexPlaylistHelper is a Dockerized solution for automating Plex media server playlists. It consists of two essential scripts: `playlist_builder.py` and `config_editor.py`, designed to streamline the process of creating dynamic playlists based on your Plex media.

## Files

1. **dockerfile**
    - Dockerfile for building the PlexPlaylistHelper image.

2. **playlist_builder.py**
    - Python script responsible for creating and refreshing Plex playlists.

3. **config_editor.py**
    - Python script providing a command-line interface for configuring Plex server settings and playlist parameters.

4. **plex_config.ini**
    - Sample configuration file for PlexPlaylistHelper.

5. **entrypoint.sh**
    - Bash script serving as the entry point for the Docker container.

## Usage

To use PlexPlaylistHelper, follow these steps:

1. Build the Docker image:
    ```bash
    docker build -t plex_playlist_helper .
    ```

2. Run the Docker container:
    ```bash
    docker run -v /path/to/plex_config.ini:/usr/src/app/plex_config.ini -v /path/to/cron/schedule:/etc/cron.d/plex_playlist_cron -it plex_playlist_helper
    ```

## Configuration

1. Adjust the plex_config.ini file to configure your Plex server settings and playlist parameters. Use config_editor.py for an interactive configuration setup.:
    ```bash
    docker exec -it <container_name_or_id> python config_editor.py    
    ```

<p align="center">
  <img src="https://github.com/desatur8/PlexPlaylistDocker/assets/53003698/a5cd58d6-fbb8-4d2e-8d1a-f3dfa59b10f9" alt="Playlist Image 1">
</p>

To create a new playlist,
- Select create a playlist
- Choose if it's individual shows or from a collection

<p align="center">
  <img src="https://github.com/desatur8/PlexPlaylistDocker/assets/53003698/20b2a716-804e-41f3-9eac-6d447096e9a8" alt="Playlist Image 2">
</p>

- Select the library where the shows are

<p align="center">
  <img src="https://github.com/desatur8/PlexPlaylistDocker/assets/53003698/9b54f41d-cd14-4e8c-957c-5d90d1cdd5bd" alt="Playlist Image 3">
</p>

- Reruns (Y/N) - Reruns will create a list of watched episodes, played randomly, (N) Will select the first unplayed episode from a season
- Number of episodes to add to the playlists
- If reruns were selected, the number of days to exclude an episode from playing again
- Select shows with space bar / (a) that you want part of the playlist

<p align="center">
  <img src="https://github.com/desatur8/PlexPlaylistDocker/assets/53003698/8138aa81-99e1-4afe-be5e-8fe1c4f96f40" alt="Playlist Image 4">
</p>




## Disclaimer

This project is provided as-is. Please ensure compatibility and reliability in your specific environment. Use at your own risk.

---


