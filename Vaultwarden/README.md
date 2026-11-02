# Vaultwarden

Self-hosted Bitwarden-compatible server. One container: SQLite is built in and
websockets run on the same port (v1.31+). All clients stay official Bitwarden
apps and extensions — in each client, set the server URL to
`https://vaultwarden.jackdawmd.duckdns.org` before logging in.

The web vault lives at the same URL.

## Deploy (on arch-server)

1. `git pull`
2. Generate the admin token hash (you type a password; that password unlocks
   `/admin` later). Copy the printed `$argon2id$...` string:
   ```
   docker run --rm -it vaultwarden/server /vaultwarden hash
   ```
3. Create `.env` in this folder. Single quotes matter:
   ```
   VAULTWARDEN_ADMIN_TOKEN='$argon2id$v=19$m=65540,t=3,p=4$...'
   ```
4. `docker compose up -d`
5. Nginx Proxy Manager: proxy host `vaultwarden.jackdawmd.duckdns.org` →
   `192.168.10.202:8222`, request a Let's Encrypt cert, Force SSL,
   WebSockets support on. No DNS change needed (AdGuard already rewrites
   `*.jackdawmd.duckdns.org` to NPM; DuckDNS serves the wildcard publicly).
6. Open the web vault, create your account while `SIGNUPS_ALLOWED=true`.
7. Close signups: in `docker-compose.yml` set `SIGNUPS_ALLOWED=false`, then
   `docker compose up -d` again.
8. Enable 2FA in the vault (TOTP or WebAuthn — no SMTP needed).

No SMTP is configured: no email invites, no login alerts, and a lost master
password has no reset path. Keep an encrypted vault export
(Tools → Export vault) somewhere safe.

## Backup

The built-in command runs `VACUUM INTO` (safe while the container runs) and
writes `db_YYYYMMDD_HHMMSS.sqlite3` into the data folder. Daily cron as
`jackdaw` on arch-server:
```
mkdir -p /mnt/lab_data/vaultwarden-backups   # once
docker exec vaultwarden /vaultwarden backup
cp ./data/db_*.sqlite3 /mnt/lab_data/vaultwarden-backups/
```

Restore: stop the container, rename the snapshot to `db.sqlite3` in `./data`,
delete any stale `db.sqlite3-wal`, start the container. Attachments and `sends`
live in `./data` too — back the whole folder up if you use attachments.
