## Setup
Click on the top left corner -> Dashboard
1. Playback - Transcoding
    - Hardware acceleration -> Nvidia NVENC
    - Enable hardware decoding for (turn these on):
        - HEVC 
        - MPEG2
        - VP9
    - Enable enhanced NVDEC decoder
    - Enable hardware encoding
    - Allow encoding in HEVC format
    - Enable tone mapping (default tone mapping algorithm)
    - Stereo Downmix Algorithm -> nightmodeDialogue
    - Encoding preset -> slow
    - Enable Delete segments and Throttle Transcodes
    - Throttle after -> 240
    - Time to keep segments -> 150
2. Playback - Trickplay
    - Enable hardware decoding
    > [!NOTE]
    > Trickplays are the images you see when you hover your mouse over the time line
    
    > [!NOTE]
    > Trickplays and chapter images need to be individually enabled for each library
3. My Plugins -> Install plugins
    - Reports
    - Playback Reporting
    - TubeArchivist: https://github.com/tubearchivist/tubearchivist-jf-plugin
   