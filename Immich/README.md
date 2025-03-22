## Setup
Click on your profile pic on the top right corner -> Administration -> Settings
1. Job Settings
    - Transcode videos concurrency -> 2
2. Video Transcoding Settings
    - Preset -> Medium
    - Hardware Acceleration
        - Acceleration API -> NVENC
        - Turn on "Hardware decoding" and "Temporal AQ"
3. Machine Learning Settings
    - Smart Search
        - CLIP model -> immich-app/XLM-Roberta-Large-ViT-H-14__frozen_laion5b_s13b_b90k (for multilingual)
