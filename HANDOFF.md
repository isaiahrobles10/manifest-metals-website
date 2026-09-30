# Handoff: Manifest Metals website

Last updated: September 30, 2026

This file is for moving the project from a personal Claude account to a business Claude account, and from Claude in the cloud to local work on a Mac in the Claude desktop app.

**Where it lives:** https://github.com/isaiahrobles10/manifest-metals-website (branch `main`). After the move in section 2, it's at `github.com/<business-account>/manifest-metals-website`.
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

## 2. Move the repo to the business GitHub account

The repo is owned by the personal GitHub account `isaiahrobles10`. The business Claude account is connected to a **different** GitHub account, so that GitHub account needs the repo. **Merge any open PRs first.**

**Recommended: transfer ownership.** The site belongs to the business, so the business GitHub account should own it. Transferring keeps all history, PRs and settings, and GitHub redirects the old repo URL.
1. Signed in as `isaiahrobles10`, open the repo → **Settings** → **General** → scroll to **Danger Zone** → **Transfer ownership**.
2. Type the business GitHub username (or organization name) as the new owner and confirm.
3. If the business account is a personal account, it gets an email asking it to accept, and it must accept within a day. If it's an organization, the transfer happens right away, as long as `isaiahrobles10` is allowed to create repos in that org.
4. The business account can't already have a repo with the same name.

After the transfer:
- **Re-check GitHub Pages** in the new repo (Settings → Pages: deploy from branch `main`, folder `/ (root)`). The site address changes to `<business-account>.github.io/manifest-metals-website/`, and the old github.io address is **not** redirected. This doesn't matter once `manifestmetals.com` is connected (section 5). On a free GitHub plan, Pages only works if the repo is **public**.
- **Point existing clones at the new home:** `git remote set-url origin https://github.com/<business-account>/manifest-metals-website.git`
- **Claude on the web** (claude.ai/code): in the business Claude account, connect the business GitHub account and install the Claude GitHub App on it, choosing this repo.
- **Claude desktop app on the Mac:** no GitHub connection inside Claude is needed. git on the Mac just has to be signed in as the business GitHub account (section 3).

**Alternatives:**
- **Add a collaborator.** Keep the repo on `isaiahrobles10` and invite the business GitHub account under Settings → Collaborators → Add people. This is quick and easy to undo, but the business never owns its own website.
- **Make a fresh copy.** Create an empty repo under the business account and push everything to it (`git push --mirror <new-url>` from a clone). This leaves the personal copy untouched, but you then have two copies that drift apart, and the PRs don't come along.

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
# use the business account's URL if you've transferred the repo (section 2)
git clone https://github.com/<business-account>/manifest-metals-website.git
cd manifest-metals-website

# 4. Prove the build works: should print "Built 19 pages" and change nothing
python3 _build/build.py
git status               # should say "nothing to commit"

# 5. Preview the site
python3 -m http.server 8000
# open http://localhost:8000 in your browser; press Ctrl+C in Terminal to stop
```

**Signing in to GitHub for pushes.** The first `git push` asks for a password, and GitHub doesn't accept your account password there. The easiest fix is **GitHub Desktop** (desktop.github.com): sign in once **with the business GitHub account** and it handles credentials. If the Mac already has the personal account saved, sign out of it first. Otherwise pushes go out as the wrong account and can be rejected. Another option is to install the GitHub CLI and run `gh auth login`.

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
