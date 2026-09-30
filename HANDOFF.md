# Handoff: Manifest Metals website

Last updated: September 30, 2026

This file is for moving the project from a personal Claude account to a business Claude account, and from Claude in the cloud to local work on a Mac in the Claude desktop app.

**Where it lives:** https://github.com/isaiahrobles10/manifest-metals-website (branch `main`)
**Technical guide for Claude:** `CLAUDE.md`, which Claude loads automatically whenever this folder is opened.

---

## 1. What moves and what doesn't

| Moves on its own (it's in the repo) | Does **not** move |
|---|---|
| Every page, photo, font, style and script | Chat history from the personal Claude account |
| The build script, with all copy, EN + ES | Links to earlier Claude sessions (they only open on the personal login) |
| Business rules for the copy (in `CLAUDE.md`) | Files that were never committed, like the high-res logo and job records |
| This handoff and the full git history | Any "memory" the personal Claude had |

Claude remembers nothing between accounts, so everything it needs has been written into `CLAUDE.md` and this file. If you teach the new Claude something important, ask it to add that to `CLAUDE.md`.

### Source material to bring over by hand
These files were used to build the site but were never in the repo. Keep them somewhere the business account can reach, such as a `source/` folder that's ignored by git, or a shared drive:
- `manifest-logo-hires.png`, the original logo the SVG emblem was traced from
- The current 26 ga color chart (12 colors)
- The job records, notes and photos behind the El Paso, Galveston and Houston write-ups
- The email signature and field forms the maroon/charcoal brand colors came from

---

## 2. Give the business Claude access to the code

Pick one:

**A. Keep the repo where it is (fastest).** The repo is owned by the GitHub user `isaiahrobles10`. Sign in to the business Claude account and connect that same GitHub account. On claude.ai this is under Settings → Connectors → GitHub. For local work on the Mac, you only need git signed in to GitHub (step 3).

**B. Move the repo to a business GitHub organization (cleaner long-term).** On GitHub, open the repo → Settings → General → Danger Zone → **Transfer ownership**, and pick the business org. GitHub redirects the old URL, but after the move you should:
- Run `git remote set-url origin https://github.com/<org>/manifest-metals-website.git` in any existing clone.
- Re-check Settings → Pages in the new location.
- Install the Claude GitHub App on the org if you want Claude on the web to open PRs.
- Note that the site's address changes from `isaiahrobles10.github.io/...` to `<org>.github.io/...` until a custom domain is set.

---

## 3. Set up the Mac

Open **Terminal** and run these one at a time:

```bash
# 1. Apple's developer tools (installs git and python3). Click "Install" in the popup.
xcode-select --install

# 2. Check they work
git --version
python3 --version        # needs 3.8 or newer

# 3. Get the code (put it wherever you like; ~/Projects is a good spot)
mkdir -p ~/Projects && cd ~/Projects
git clone https://github.com/isaiahrobles10/manifest-metals-website.git
cd manifest-metals-website

# 4. Prove the build works: should print "Built 19 pages" and change nothing
python3 _build/build.py
git status               # should say "nothing to commit"

# 5. Preview the site
python3 -m http.server 8000
# open http://localhost:8000 in your browser; press Ctrl+C in Terminal to stop
```

**Signing in to GitHub for pushes.** The first `git push` asks for a password, and GitHub doesn't accept your account password there. The easiest fix is **GitHub Desktop** (desktop.github.com): sign in once and it handles credentials. Another option is to install the GitHub CLI and run `gh auth login`.

No npm, Node, Homebrew or other packages are needed.

---

## 4. Open it in the Claude desktop app

1. Install the Claude desktop app for Mac from claude.ai/download and sign in with the **business** account.
2. Go to the **Code** tab and choose the `~/Projects/manifest-metals-website` folder as the working folder.
3. Claude reads `CLAUDE.md` automatically. A good first message:

   > Read CLAUDE.md and HANDOFF.md, run the build, and tell me the state of the site and the open items.

4. Ask Claude to preview changes with `python3 -m http.server 8000`, and to commit and push when you're happy with them.

The Claude Code CLI works the same way (`claude` run inside the folder), and so do the VS Code / Cursor extensions.

---

## 5. How the site is published

- **Host:** GitHub Pages, serving the `main` branch from the repo root. `.nojekyll` tells Pages not to process the files. There's no build step on GitHub, so the generated HTML must be committed.
- **Domain:** the code is written for **https://manifestmetals.com**. Canonical links, the sitemap, `robots.txt` and schema all use that domain. The `CNAME` file was **removed on purpose** on Sep 25, 2026 ("site still in progress"), so right now Pages serves the site at its github.io address.
- **To go live on the domain:**
  1. Recreate `CNAME` with the single line `manifestmetals.com`, or set the custom domain in repo Settings → Pages.
  2. At the domain registrar, point DNS to GitHub Pages: four `A` records for the apex (185.199.108.153, .109.153, .110.153, .111.153) and a `CNAME` for `www` → `<owner>.github.io`.
  3. Turn on **Enforce HTTPS** in Settings → Pages once the certificate is issued.
- **Quote form:** it sends leads through FormSubmit to **manifestmetalsep@gmail.com**. The first real submission sends a one-time activation email to that inbox, and nothing arrives until someone clicks it. If leads should go to a new business address, change `EMAIL` in `_build/build.py`, rebuild, push, and activate again from the new inbox.

---

## 6. History

| Date | What happened |
|---|---|
| Sep 25, 2026 | First version of the site, then real project photos with a gallery and lightbox (Houston area, El Paso R-panel re-roof, Galveston standing seam) |
| Sep 25 | Custom domain added, then removed until the site is finished |
| Sep 25 | Full review: real logo and brand colors, content checked against job records, the 12 real chart colors in the visualizer, new "Our Work" and "Shingle to Metal" pages, working quote form, FAQ and breadcrumb schema, zero axe accessibility violations |
| Sep 26 | Changes from an outside review: home page cut by about a third on phones, careful insurance/lifespan wording, visualizer color carries into the quote form, commercial-only fields on the form, new privacy page |

Pages (EN / ES): Home, Residential / Residencial, Commercial / Comercial, Our Work / Proyectos, Shingle to Metal / De tejas a metal, Standing Seam vs R-Panel guide, About / Nosotros, Contact / Contacto, Privacy / Privacidad, plus a 404 page.

---

## 7. Open items

Roughly in priority order:

1. **Activate the quote form.** Send one test from `/contact/`, click the FormSubmit activation email in manifestmetalsep@gmail.com, then send a second test to confirm it arrives. Decide whether leads should go to a business email instead.
2. **Decide on hosting and domain.** Reconnect `manifestmetals.com` when ready (section 5). Until then, links in shared previews and the sitemap point at a domain that isn't serving this site yet.
3. **The 404 page on github.io.** The 404 page uses root-absolute paths (`/assets/...`). They work on the custom domain but break its styling at `<owner>.github.io/manifest-metals-website/`. This goes away once the domain is connected.
4. **Verify, then consider adding:** Texas license or registration details, insurance and bonding, warranty terms, and reviews. The copy rules block all of these until the owner confirms them.
5. **More projects:** each new job needs real photos (resized to WebP at the widths in `IMAGES`) and a write-up with no customer name or address.
6. **Analytics:** none installed. If you add some, update the privacy page (it says so on the page).
7. **Google Business Profile, Search Console and Bing Webmaster:** submit `sitemap.xml` once the domain is live.

---

## 8. Business facts used on the site

- **Company:** Manifest Metals, LLC, El Paso County, Texas. Locally owned. Se habla español.
- **Phone:** (915) 861-6436
- **Email:** manifestmetalsep@gmail.com
- **Services:** standing seam and R-panel metal roofing, shingle-to-metal conversions, metal wall panels and siding, commercial bids for GCs, architects and owners
- **Service area:** El Paso, Horizon City, Socorro, San Elizario, Clint, Fabens, Canutillo, Vinton, Anthony TX, plus projects across Texas (Galveston, Houston area)

If any of these change, update the constants at the top of `_build/build.py` and rebuild.
