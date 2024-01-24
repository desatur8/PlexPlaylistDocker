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

## Disclaimer

This project is provided as-is. Please ensure compatibility and reliability in your specific environment. Use at your own risk.

---


