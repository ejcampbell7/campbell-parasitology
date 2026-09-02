# Setup guide

This is a Jekyll site, built to run on **GitHub Pages with no build step
required on your end** — you push Markdown files, and GitHub builds and
publishes the site automatically (via the GitHub Actions workflow in
`.github/workflows/deploy.yml`, which also keeps your Publications page
in sync with your ORCID record — see step 5). You don't need to install
anything to use it day-to-day.

## 1. Create the GitHub repository

1. Go to [github.com/new](https://github.com/new) (sign in first if needed).
2. **Repository name:** since this site will live at your own domain
   (`campbellparasitology.org` — see step 4), the repo name itself doesn't
   matter for the URL. Pick anything, e.g. `campbell-lab-website`.
3. Set it to **Public** (GitHub Pages requires this on free accounts).
4. Do **not** check "Add a README" — this project already has one.
5. Click **Create repository**.

## 2. Upload this site

**Easiest option (no command line): use GitHub's web upload.**

1. On your new repo's page, click **"uploading an existing file"**.
2. Drag the entire contents of this folder (everything *inside*
   `campbell-lab-site/`, not the folder itself) into the browser window.
   You'll need to do this in a few batches since GitHub's uploader doesn't
   always handle nested folders well from drag-and-drop — if a folder like
   `_layouts` doesn't upload as a folder, use the command-line option below
   instead.
3. Commit directly to the `main` branch.

**Command-line option (more reliable for nested folders):**

```bash
cd campbell-lab-site
git init
git add .
git commit -m "Initial site"
git branch -M main
git remote add origin https://github.com/ejcampbell7/YOUR-REPO-NAME.git
git push -u origin main
```

(If you don't have `git` installed, install [GitHub Desktop](https://desktop.github.com/)
instead — it lets you do all of this by clicking buttons rather than typing
commands: "Add local repository" → point it at this folder → "Publish
repository.")

## 3. Turn on GitHub Pages

This site builds via GitHub Actions (not GitHub's plain Jekyll build),
because that's what lets it pull in your ORCID publications automatically.

1. In your repo, go to **Settings → Pages**.
2. Under "Build and deployment", set **Source** to **GitHub Actions**
   (not "Deploy from a branch").
3. Go to the **Actions** tab. You should see a workflow run called
   "Build and deploy site" — if it's not running automatically, click
   into it and use **Run workflow**.
4. Once it finishes (green check, ~1–2 minutes), go back to
   **Settings → Pages** — GitHub will show your live URL at the top
   (something like `https://ejcampbell7.github.io/YOUR-REPO-NAME/`,
   until you connect your own domain in step 4).

Don't worry if the first run's publications step shows a warning — that's
expected until you complete step 5 below.

## 4. Connect campbellparasitology.org

`_config.yml` and the `CNAME` file are already set up for this domain —
you just need to buy it and point it at GitHub. If you haven't bought it
yet, do that first (any registrar; ~$12-15/yr for `.org`) — see the
availability caveat from earlier: it was unregistered when checked, but
isn't reserved for you until you buy it.

1. **At your registrar**, add these DNS records for the domain:
   - Four `A` records (root/`@`) → `185.199.108.153`, `185.199.109.153`,
     `185.199.110.153`, `185.199.111.153`
   - One `CNAME` record for `www` → `ejcampbell7.github.io`
2. **In the repo**, go to **Settings → Pages**, and under "Custom domain"
   enter `campbellparasitology.org`, then Save. (The `CNAME` file already
   in the repo does most of this automatically, but entering it here too
   makes GitHub issue the HTTPS certificate.)
3. Wait for DNS to propagate (can take anywhere from a few minutes to a
   few hours), then check the box for **Enforce HTTPS** once it becomes
   available.
4. Also update `contact_email` and `address` near the top of `_config.yml`
   while you're in there.

**For FR3's domain (`fr3resource.org`):** once you've bought it, set up
**domain forwarding** at that registrar (most offer this as a free/cheap
built-in feature — no DNS records like above needed) pointing to
`https://campbellparasitology.org/fr3/`. That's entirely a registrar-side
setting; nothing to change in this repo for it.

## 5. Set up automatic ORCID sync

This makes the Publications page pull directly from your ORCID record —
no manual editing needed for papers already on ORCID. It runs on every
push and once a week on its own (so a paper you add to ORCID later shows
up here within a week even if you don't touch the repo), and you can also
trigger it manually any time from the Actions tab.

1. **Get free ORCID API credentials** (2 minutes, one time):
   - Sign in at [orcid.org](https://orcid.org) and go to
     [orcid.org/developer-tools](https://orcid.org/developer-tools).
   - Click **"Register for the free ORCID public API"** and fill in the
     short form (application name — e.g. "Campbell Lab website" —
     and a website URL; for **redirect URI** you can put your GitHub
     Pages URL, or `https://github.com` if you're not sure yet — it isn't
     actually used for this kind of sync).
   - You'll get a **Client ID** and **Client Secret**. Keep this page open.
2. **Add them to the repo as secrets** (so they're never public):
   - In your repo, go to **Settings → Secrets and variables → Actions**.
   - Click **New repository secret**. Name: `ORCID_CLIENT_ID`, value: the
     Client ID from step 1. Save.
   - Repeat for `ORCID_CLIENT_SECRET` with your Client Secret.
3. **ORCID iD:** already set to `0000-0003-1096-1510` in both `_config.yml`
   and `_people/elyssa-campbell.md` in this copy of the site — nothing to
   do here unless it ever changes.
4. **Trigger a sync:** go to the **Actions** tab → "Build and deploy site"
   → **Run workflow**. When it finishes, your Publications page should
   show your ORCID works.

If a sync run ever fails (e.g. ORCID is briefly down), the site still
builds and deploys — it just keeps whatever publications were generated
last time, plus anything you've added by hand.

---

# Adding content later

Everything below can be done **entirely on github.com** — click into a
file, click the pencil ("Edit") icon, make changes, and click "Commit
changes." No software required. Each change rebuilds the live site
automatically in about a minute.

## Add a news post

Create a new file in `_posts/` named `YYYY-MM-DD-a-short-title.md`
(the date in the filename controls where it sorts), with this template:

```markdown
---
title: "Your headline here"
---

Your post content, in plain text or Markdown (you can **bold**, add
[links](https://example.com), etc.)
```

It will automatically appear on the **News** page and the homepage.

## Add a publication

Anything on your ORCID record appears automatically once weekly sync
setup is done (see step 5 above) — those files are named `orcid-*.md`
and get regenerated each sync, so don't hand-edit them.

To add something ORCID doesn't have yet (a preprint, an in-press paper),
create a new file in `_publications/` named anything that does **not**
start with `orcid-` (e.g. `2027-your-paper.md`), with this template:

```markdown
---
title: "Full paper title"
authors: "Last F, Last F, Campbell E"
year: 2027
journal: "Journal Name"
citation: "Journal Name, Volume(Issue), pages (2027)"
doi: "10.xxxx/xxxxx"
external_url: "https://doi.org/10.xxxx/xxxxx"
category: "Heartworm"   # or "Filariasis", "Hookworm", "FR3", etc — for your own reference
order: 1
---

One or two sentences summarizing the paper (optional).
```

It will automatically appear on the **Publications** page, sorted by year.

## Add a team member

Create a new file in `_people/`, named e.g. `first-last.md`:

```markdown
---
title: "Full Name, degree"
role: "Their role, e.g. PhD Student"
order: 2   # controls sort order on the People page; PI is order: 1
photo: ""  # optional — see below
---

A short bio paragraph.
```

**To add a photo:** put an image file in `assets/images/people/` (create
that folder if it doesn't exist), then set `photo:` above to its path,
e.g. `photo: /assets/images/people/first-last.jpg`.

## Add an FR3 SOP

Open `fr3/sops.md`, and either:
- Add a row to the table with a link to a PDF you've uploaded to
  `assets/files/sops/`, or
- If the list grows past ~10 SOPs, it's worth converting this into its
  own collection (like Publications) — just ask for that when you're
  ready.

## Editing existing pages

`research.md`, `people.md` (the intro text), `contact.md`, `fr3/index.md`,
and `fr3/resources.md` are all plain Markdown files at the top level (or
in `fr3/`) — open, edit, commit.

## Changing colors/logo

This site actually carries **two** brands, and pages switch between them
automatically based on the URL — you don't have to do anything per-page:

- Every page **except** `/fr3/*` uses the **Campbell Parasitology Lab**
  colors and fonts, set in the `:root { ... }` block near the top of
  `assets/css/main.css`.
- Every page **under `/fr3/`** (FR3's overview, resources, and SOPs pages)
  automatically switches to **FR3's** own colors and fonts, set in the
  `.fr3-section { ... }` block right below it — this revives FR3's
  historical navy-and-cyan look. The switch is driven by
  `_layouts/default.html` checking the page URL, so a new page you create
  under `fr3/` will pick up FR3's branding automatically.

To re-theme either brand, change the hex codes in the matching block —
nothing else in the CSS needs to change, since every other rule reads
color from these variables.

**Logos:** `assets/images/logo.svg` is the lab mark (used everywhere
except `/fr3/` pages); `assets/images/fr3-logo.svg` is FR3's own mark
(used only on `/fr3/` pages) — both are plain text files you or I can
edit directly, or replace with your own images (update the `<img>`
references in `_includes/header.html` if you change either filename).
`assets/images/favicon.svg` is the browser-tab icon for the whole site
(there's only one, since it's one domain).

## Trying it locally (optional)

Not required — GitHub builds the site for you. But if you ever want to
preview changes before pushing, with [Ruby](https://www.ruby-lang.org/)
installed:

```bash
bundle install
bundle exec jekyll serve
```

Then open `http://localhost:4000`.
