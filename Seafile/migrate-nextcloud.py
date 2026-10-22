#!/usr/bin/env python3
"""Copy a Nextcloud user-files tree into a Seafile library over the REST API.

Runs inside the seafile container (needs requests + network access to 127.0.0.1).

The upload-link endpoint returns a URL built from SEAFILE_SERVER_PROTOCOL and
SEAFILE_SERVER_HOSTNAME (https://<public host>/seafhttp/...). Inside the
container that host is not reachable, so the URL is rewritten to the local
nginx. Pass --rewrite-from/--rewrite-to to change that mapping.

Existing files are skipped when their size already matches, so the copy is
resumable after an interruption.

Example (inside the container):
  python3 /tmp/migrate-nextcloud.py \
      --source /nc/admin/files --library admin \
      --user admin@jackdawmd.duckdns.org --password-file /tmp/seafile.pw
"""
import argparse
import os
import sys
import time

import requests

PUBLIC_PREFIX = "https://seafile.jackdawmd.duckdns.org/seafhttp/"
LOCAL_PREFIX = "http://127.0.0.1/seafhttp/"


def api(base, token):
    s = requests.Session()
    s.headers["Authorization"] = "Token " + token
    return s


def login(base, user, password):
    r = requests.post(base + "/api2/auth-token/",
                      data={"username": user, "password": password}, timeout=60)
    r.raise_for_status()
    return r.json()["token"]


def find_or_create_library(sess, base, name):
    for repo in sess.get(base + "/api2/repos/", timeout=60).json():
        if repo["name"] == name:
            return repo["id"]
    r = sess.post(base + "/api2/repos/", data={"name": name,
                                              "desc": "migrated from Nextcloud"},
                  timeout=60)
    r.raise_for_status()
    return r.json()["repo_id"]


def listing(sess, base, repo, path):
    r = sess.get(base + "/api2/repos/%s/dir/?p=%s" % (repo, path), timeout=120)
    if r.status_code != 200:
        return {}
    return {e["name"]: e for e in r.json()}


def mkdir(sess, base, repo, path):
    r = sess.post(base + "/api2/repos/%s/dir/?p=%s" % (repo, path),
                  data={"operation": "mkdir"}, timeout=120)
    if r.status_code not in (200, 201):
        print("  mkdir failed %s: %s %s" % (path, r.status_code, r.text[:120]))


def upload(sess, base, repo, parent, local_path, name):
    link = sess.get(base + "/api2/repos/%s/upload-link/?p=%s" % (repo, parent),
                    timeout=120).json()
    link = link.replace(PUBLIC_PREFIX, LOCAL_PREFIX)
    with open(local_path, "rb") as fh:
        r = requests.post(link, files={"file": (name, fh)},
                          data={"parent_dir": parent}, timeout=24 * 3600)
    if r.status_code != 200:
        raise RuntimeError("upload of %s failed: %s %s"
                           % (local_path, r.status_code, r.text[:200]))
    return r.text.strip()


def walk(sess, base, repo, source, remote_dir, stats):
    entries = sorted(os.listdir(source))
    existing = listing(sess, base, repo, remote_dir)
    for entry in entries:
        local = os.path.join(source, entry)
        remote = remote_dir.rstrip("/") + "/" + entry
        if os.path.isdir(local):
            if entry not in existing:
                mkdir(sess, base, repo, remote)
            walk(sess, base, repo, local, remote, stats)
            continue
        if not os.path.isfile(local):
            print("  skip non-regular file:", local)
            continue
        size = os.path.getsize(local)
        have = existing.get(entry)
        if have and have.get("size") == size:
            stats["skipped"] += 1
            stats["bytes_skipped"] += size
            continue
        started = time.time()
        upload(sess, base, repo, remote_dir, local, entry)
        stats["uploaded"] += 1
        stats["bytes_uploaded"] += size
        rate = size / max(time.time() - started, 0.001) / 1e6
        print("  + %s (%.1f MB, %.1f MB/s) [%d files, %.2f GB]"
              % (remote, size / 1e6, rate, stats["uploaded"],
                 stats["bytes_uploaded"] / 1e9))
        sys.stdout.flush()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--library", required=True)
    ap.add_argument("--user", required=True)
    ap.add_argument("--password")
    ap.add_argument("--password-file")
    ap.add_argument("--base", default="http://127.0.0.1")
    ap.add_argument("--target-dir", default="/")
    args = ap.parse_args()

    password = args.password
    if not password and args.password_file:
        with open(args.password_file) as fh:
            password = fh.read().strip()
    if not password:
        sys.exit("no password given")

    token = login(args.base, args.user, password)
    sess = api(args.base, token)
    repo = find_or_create_library(sess, args.base, args.library)
    print("library %s -> %s" % (args.library, repo))

    stats = {"uploaded": 0, "skipped": 0, "bytes_uploaded": 0,
             "bytes_skipped": 0}
    started = time.time()
    walk(sess, args.base, repo, args.source, args.target_dir, stats)
    print("done: %d uploaded (%.2f GB), %d skipped (%.2f GB) in %.0fs"
          % (stats["uploaded"], stats["bytes_uploaded"] / 1e9,
             stats["skipped"], stats["bytes_skipped"] / 1e9,
             time.time() - started))


if __name__ == "__main__":
    main()
