#Use an official python runtime as the parent image
FROM python:3.8-slim

#install cron to run the scripts
RUN apt-get update && apt-get install -y cron

#working directoty for the scripts
WORKDIR /usr/src/app

#set the timezone
ENV TZ=Africa/Johannesburg

#copying the needed scripts
#the python script that will be building out the playlists
COPY playlist_builder.py .
#configuration script that will allow the user to choose plex server, playlists, etc
COPY config_editor.py .
#the shell script that will be run by cron
COPY entrypoint.sh .
#shell script that lets cron start with the correct cron file
#removing start_sh, testing in cmd
#COPY start_cron.sh .

#installing dependencies
RUN pip install plexapi questionary colorama

#make the shell scripts executable
RUN chmod +x entrypoint.sh
#RUN chmod +x start_cron.sh

#set the timezone, and start the cron 
# Set the timezone, run crontab, and run cron in the foreground
CMD ["sh", "-c", "ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && crontab /etc/cron.d/plex_playlist_cron && cron -f"]
