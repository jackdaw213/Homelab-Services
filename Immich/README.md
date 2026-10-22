## Setup
Click on your profile pic on the top right corner -> Administration -> Settings
1. Job Settings
    - Transcode videos concurrency -> 2
2. Video Transcoding Settings
    - Preset -> Medium
    - Hardware Acceleration
        - Nvidia
            - Acceleration API -> NVENC
            - Turn on "Hardware decoding" and "Temporal AQ"
        - Intel
            - Acceleration API -> Quick Sync
3. Machine Learning Settings
    - Smart Search
        - CLIP model -> ViT-SO400M-16-SigLIP2-384__webli (for multilingual)
