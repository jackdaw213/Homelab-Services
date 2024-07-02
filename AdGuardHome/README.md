## Setup
1. Add host's ip address to router DNS setting
2. Settings
    - Filters 
        - DNS rewrites
            - *.jackdawmd.duckdns.org - <host's ip address>
        - DNS blocklists
            - Enable: AdAway Default Blocklist
            - Add: VNM ABPVN List
    - Settings 
        - DNS settings
            - Upstream DNS servers
                - https://dns.cloudflare.com/dns-query
                - https://dns10.quad9.net/dns-query
            - Enable: Parallel requests
        - DNS cache configuration
            - Cache size: 33554432
            - Override minimum TTL: 2400
            - Override maximum TTL: 84600
