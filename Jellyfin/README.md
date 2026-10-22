## Setup
Click on the top left corner -> Dashboard
1. Playback - Transcoding
    - Nvidia
        - Hardware acceleration -> Nvidia NVENC
        - Enable hardware decoding for (turn these on):
            - HEVC 
            - MPEG2
            - VP9
        - Enable enhanced NVDEC decoder
        - Enable hardware encoding
        - Allow encoding in HEVC format
        - Enable tone mapping (default tone mapping algorithm)
    - Intel
        - Hardware acceleration -> Intel QuickSync
        - Enable hardware decoding for ALL except VP8 (If your GPU does not have AV1 decoder turn it off)
        - Enable Prefer OS native DXVA or VA-API hardware decoders
        - Enable both Low-Power encoding options (Enable GuC/HuC on host VM)
        - Allow encoding in HEVC/AV1 format (If your GPU does not have AV1 encoder turn it off)
        - Enable VPP tone mapping
    - Stereo Downmix Algorithm -> nightmodeDialogue
    - Encoding preset -> slow
    - Enable Delete segments and Throttle Transcodes
    - Cache (this will use roughly 1.5-2GB of vram, increase or decrease how ever you like)
        - Throttle after -> 240
        - Time to keep segments -> 150
2. Playback - Trickplay
    - Enable hardware decoding
    - Enable hardware accelerated MJPEG encoding if not using Nvidia GPU
    > [!NOTE]
    > Trickplays are the images you see when you hover your mouse over the time line
    
    > [!NOTE]
    > Trickplays and chapter images need to be individually enabled for each library
3. My Plugins -> Install plugins
    - Reports
    - Playback Reporting
    - TubeArchivist: https://github.com/tubearchivist/tubearchivist-jf-plugin
   