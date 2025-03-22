## Setup 
Go to the Settings tab on the left and change these settings
1. Languages
    - Subtitles Language -> Languages Filter -> Add English
    - Languages Profile -> Add New Profile 
        - Add Language -> English -> Save
    - Scroll down and set the profile as default for both series and movies
2. Providers
    - Gestdown
    - OpenSubtitles: You will need to create an account with OpenSubtitles
    - Embedded Subtitles: Set timeout to 900 seconds if you have reeeeally slow IO (ex. Portable USB HDD)
3. Subtitle
    - Embedded Subtitles Handling: Turn off "Show Only Desired Languages"
    - Audio Synchronization / Alignment: Enable "Automatic Subtitles Synchronization"
4. Enable Sonarr and Radarr
    - Host -> At address put in the container name since we are using docker
        - Example: Set the address as "sonarr" if you set "container_name: sonarr" in Sonarr's docker compose file
    - Options -> Download only monitored
5. Scheduler
    - Sonarr/Radarr Sync -> Turn on all "Sync Only Monitored" options

## Reference
- [Bazarr Wiki - Getting Started/First-time Installation Configuration](https://wiki.bazarr.media/Getting-Started/First-time-installation-configuration/)
