#!/usr/bin/env node
// Set URI match detection = Host (1) on every vault item under *.jackdawmd.duckdns.org.
//
// Why: Bitwarden's default "Base domain" matching offers all lab logins on every
// lab subdomain (jackdawmd.duckdns.org is a Public Suffix List registrable domain).
// The per-URI "Host" flag fixes that. This script applies it in bulk.
//
// Why two paths: the `bw` CLI cannot persist per-URI match flags (it sends the
// wrong field name), but it is needed to regenerate uriChecksums, which only a
// client holding the user key can compute. So: CLI re-save (checksums) then a
// direct API write (match flag), which preserves the fresh checksums.
//
// Usage:
//   1. bw login --raw > ~/.cache/bw-session   (or bw unlock --raw if already logged in)
//   2. BITWARDENCLI_APPDATA_DIR=~/.cache/bwcli/appdata \
//      BW_SESSION=$(cat ~/.cache/bw-session) node set-host-match.mjs
//   3. Delete the session file when done.
//
// Requires: @bitwarden/cli installed at ~/.cache/bwcli (npm install --prefix ~/.cache/bwcli @bitwarden/cli)

import { execFileSync } from "child_process";
import fs from "fs";

const DOMAIN = "jackdawmd.duckdns.org";
const BASE = process.env.VAULTWARDEN_URL || `https://vaultwarden.${DOMAIN}`;
const BW = process.env.BW_BIN || `${process.env.HOME}/.cache/bwcli/node_modules/.bin/bw`;
const APPDATA = process.env.BITWARDENCLI_APPDATA_DIR || `${process.env.HOME}/.cache/bwcli/appdata`;

const session = process.env.BW_SESSION;
if (!session) { console.error("BW_SESSION not set. See usage in the file header."); process.exit(1); }

const run = (args, input) => execFileSync(BW, args, { input, encoding: "utf8", maxBuffer: 64 * 1024 * 1024 }).trim();

console.log("sync:", run(["sync"]));

// access token for direct API writes (kept in memory, never printed)
const dataJson = JSON.parse(fs.readFileSync(`${APPDATA}/data.json`, "utf8"));
const tokenKey = Object.keys(dataJson).find(k => k.endsWith("_token_accessToken") && dataJson[k]);
if (!tokenKey) { console.error("No access token in data.json — is the CLI logged in?"); process.exit(1); }
const uid = tokenKey.split("_")[1];
const H = { Authorization: `Bearer ${dataJson[tokenKey]}`, "Content-Type": "application/json" };

const isLab = u => (u?.uri || "").includes(DOMAIN);
const items = JSON.parse(run(["list", "items", "--raw"]))
  .filter(i => i.type === 1 && (i.login?.uris || []).some(isLab));
console.log("items to fix:", items.length);

let ok = 0, fail = 0;
for (const it of items) {
  try {
    // 1. CLI re-save: regenerate ciphertext + uriChecksum, no match flags
    const obj = JSON.parse(run(["get", "item", it.id, "--raw"]));
    obj.login = obj.login || {};
    const plainUris = (obj.login.uris || []).map(u => u.uri);
    if (!plainUris.length) { console.log("SKIP (no uris) " + it.name); continue; }
    obj.login.uris = plainUris.map(uri => ({ uri }));
    run(["edit", "item", it.id], run(["encode"], JSON.stringify(obj)));

    // 2. direct API write: add match=1 to lab URIs, preserve checksums
    const cur = await (await fetch(`${BASE}/api/ciphers/${it.id}`, { headers: H })).json();
    const login = JSON.parse(JSON.stringify(cur.login));
    delete login.response;
    login.uris = (login.uris || []).map((u, i) => ({
      uri: u.uri,
      match: isLab({ uri: plainUris[i] }) ? 1 : (u.match ?? null),
      ...(u.uriChecksum ? { uriChecksum: u.uriChecksum } : {}),
    }));
    const body = {
      id: cur.id, organizationId: cur.organizationId ?? null, folderId: cur.folderId ?? null,
      encryptedFor: uid, type: cur.type, name: cur.name,
      notes: cur.notes ?? null, fields: cur.fields ?? null, login,
      favorite: !!cur.favorite, reprompt: cur.reprompt ?? 0,
      passwordHistory: cur.passwordHistory ?? null,
      lastKnownRevisionDate: cur.revisionDate,
    };
    if (cur.key !== undefined) body.key = cur.key;
    const r = await fetch(`${BASE}/api/ciphers/${it.id}`, { method: "PUT", headers: H, body: JSON.stringify(body) });
    if (r.ok) { ok++; console.log("OK   " + it.name); }
    else { fail++; console.log("FAIL " + r.status + " " + it.name); }
  } catch (e) {
    fail++; console.log("ERR  " + it.name + " :: " + String(e.message || e).split("\n")[0].slice(0, 120));
  }
}
console.log(`done: ok=${ok} fail=${fail}. Delete the session file when finished.`);
