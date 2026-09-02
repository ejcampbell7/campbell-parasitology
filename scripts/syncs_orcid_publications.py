#!/usr/bin/env python3
"""
Pulls works from an ORCID public record and writes them into _publications/
as Markdown files with front matter matching the site's publication layout.

Runs in GitHub Actions (see .github/workflows/deploy.yml) before the Jekyll
build, so the Publications page always reflects the current ORCID record.

Requires two secrets (set in the GitHub repo under Settings > Secrets and
variables > Actions):
  ORCID_CLIENT_ID
  ORCID_CLIENT_SECRET
(Free to obtain — see SETUP.md, "Set up automatic ORCID sync".)

Reads the ORCID iD itself from _config.yml (the `orcid:` field), so there's
only one place to set/update it.

Only manages files it created (named orcid-<put-code>.md) — anything added
by hand in _publications/ is left alone.

Uses only the Python standard library so no extra install step is needed
in CI.
"""

from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "_config.yml"
PUBLICATIONS_DIR = ROOT / "_publications"

TOKEN_URL = "https://orcid.org/oauth/token"
API_BASE = "https://pub.orcid.org/v3.0"


def fail(msg: str) -> "None":
    print(f"::error::{msg}", file=sys.stderr)
    sys.exit(1)


def get_orcid_id_from_config() -> str:
    text = CONFIG_PATH.read_text(encoding="utf-8")
    m = re.search(r'^orcid:\s*["\']?([0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[0-9X])["\']?\s*$',
                   text, re.MULTILINE)
    if not m:
        fail(
            "Could not find a valid `orcid:` field in _config.yml. "
            "Add a line like: orcid: \"0000-0002-1825-0097\""
        )
    return m.group(1)


def http_json(url: str, data: bytes | None = None, headers: dict | None = None) -> dict:
    req = urllib.request.Request(url, data=data, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        fail(f"Request to {url} failed: HTTP {e.code}\n{body}")
    except urllib.error.URLError as e:
        fail(f"Request to {url} failed: {e.reason}")


def get_access_token(client_id: str, client_secret: str) -> str:
    body = urllib.parse.urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
        "scope": "/read-public",
    }).encode("utf-8")
    resp = http_json(
        TOKEN_URL,
        data=body,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
    )
    token = resp.get("access_token")
    if not token:
        fail(f"No access_token in ORCID token response: {resp}")
    return token


def api_get(path: str, token: str) -> dict:
    return http_json(
        f"{API_BASE}{path}",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
    )


def safe_get(d: dict, *path, default=None):
    cur = d
    for key in path:
        if not isinstance(cur, dict) or cur.get(key) is None:
            return default
        cur = cur[key]
    return cur


def extract_doi_and_url(summary: dict) -> tuple[str | None, str | None]:
    ext_ids = safe_get(summary, "external-ids", "external-id", default=[]) or []
    doi = None
    for eid in ext_ids:
        if (eid.get("external-id-type") or "").lower() == "doi":
            doi = eid.get("external-id-value")
            break
    if doi:
        return doi, f"https://doi.org/{doi}"
    # Fall back to the work's own URL, or the first external id URL available.
    work_url = safe_get(summary, "url", "value")
    if work_url:
        return None, work_url
    for eid in ext_ids:
        u = safe_get(eid, "external-id-url", "value")
        if u:
            return None, u
    return None, None


def extract_authors(token: str, orcid_id: str, put_code: int) -> str | None:
    try:
        full = api_get(f"/{orcid_id}/work/{put_code}", token)
    except SystemExit:
        # api_get already logged the error via fail(); don't kill the whole
        # sync over one work's contributor list.
        return None
    contributors = safe_get(full, "contributors", "contributor", default=[]) or []
    names = []
    for c in contributors:
        role = safe_get(c, "contributor-attributes", "contributor-role")
        if role and role.upper() != "AUTHOR":
            continue
        name = safe_get(c, "credit-name", "value")
        if name:
            names.append(name)
    return ", ".join(names) if names else None


def slugify(text: str, max_len: int = 60) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:max_len].rstrip("-") or "untitled"


def build_markdown(title: str, authors: str | None, year: str | None, journal: str | None,
                    doi: str | None, url: str | None, put_code: int) -> str:
    def yaml_str(s: str) -> str:
        return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'

    citation_parts = [p for p in [journal, f"({year})" if year else None] if p]
    citation = " ".join(citation_parts) if citation_parts else ""

    lines = ["---"]
    lines.append(f"title: {yaml_str(title)}")
    if authors:
        lines.append(f"authors: {yaml_str(authors)}")
    if year:
        lines.append(f"year: {year}")
    if journal:
        lines.append(f"journal: {yaml_str(journal)}")
    if citation:
        lines.append(f"citation: {yaml_str(citation)}")
    if doi:
        lines.append(f"doi: {yaml_str(doi)}")
    if url:
        lines.append(f"external_url: {yaml_str(url)}")
    lines.append(f"orcid_put_code: {put_code}")
    lines.append("source: orcid")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    import os

    client_id = os.environ.get("ORCID_CLIENT_ID")
    client_secret = os.environ.get("ORCID_CLIENT_SECRET")
    if not client_id or not client_secret:
        fail(
            "ORCID_CLIENT_ID / ORCID_CLIENT_SECRET are not set. "
            "Add them as repository secrets — see SETUP.md."
        )

    orcid_id = get_orcid_id_from_config()
    print(f"Syncing publications for ORCID iD {orcid_id}...")

    token = get_access_token(client_id, client_secret)
    works = api_get(f"/{orcid_id}/works", token)
    groups = works.get("group", [])
    print(f"Found {len(groups)} work group(s) on the ORCID record.")

    PUBLICATIONS_DIR.mkdir(exist_ok=True)
    seen_put_codes = set()

    for group in groups:
        summaries = group.get("work-summary", [])
        if not summaries:
            continue
        summary = summaries[0]  # representative entry for this work group

        put_code = summary.get("put-code")
        title = safe_get(summary, "title", "title", "value")
        if not title or put_code is None:
            continue
        year = safe_get(summary, "publication-date", "year", "value")
        journal = safe_get(summary, "journal-title", "value")
        doi, url = extract_doi_and_url(summary)
        authors = extract_authors(token, orcid_id, put_code)

        seen_put_codes.add(put_code)
        filename = f"orcid-{put_code}-{slugify(title)}.md"
        content = build_markdown(title, authors, year, journal, doi, url, put_code)
        (PUBLICATIONS_DIR / filename).write_text(content, encoding="utf-8")

    # Remove previously-generated files for works no longer on the record.
    # Files not managed by this script (no "orcid-" prefix) are left alone.
    removed = 0
    for existing in PUBLICATIONS_DIR.glob("orcid-*.md"):
        text = existing.read_text(encoding="utf-8")
        m = re.search(r"^orcid_put_code:\s*(\d+)\s*$", text, re.MULTILINE)
        if m and int(m.group(1)) not in seen_put_codes:
            existing.unlink()
            removed += 1

    print(f"Wrote {len(seen_put_codes)} publication(s); removed {removed} stale file(s).")


if __name__ == "__main__":
    main()
