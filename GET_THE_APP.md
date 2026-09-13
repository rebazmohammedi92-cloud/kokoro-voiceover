# Getting the actual app, with no Windows PC needed

This folder includes a GitHub Actions workflow that builds the real
`KokoroVoiceover-Setup.exe` for you, on GitHub's own (free) Windows
servers. You just upload this folder and click one button.

## Steps

1. Go to https://github.com/new and create a repo (public is simplest —
   free Actions minutes are unlimited on public repos). Name it anything,
   e.g. `kokoro-voiceover`.

2. Upload every file in this zip to that repo, **keeping the folder
   structure** — the `.github/workflows/build-installer.yml` file must
   stay at that exact path. Easiest way: on the repo page, click
   "Add file → Upload files", drag in the whole extracted folder
   (including the hidden `.github` folder — if your file browser hides
   it, use `git` instead: `git add -A && git commit -m "add app" && git push`).

3. Click the **Actions** tab on your repo → select
   **"Build Kokoro Voiceover Installer"** on the left → click
   **"Run workflow"** (green button) → **Run workflow** again to confirm.

4. Wait about 5–10 minutes for it to finish (it shows a spinner, then a
   green check).

5. Click into the finished run → scroll down to **Artifacts** →
   download **KokoroVoiceover-Setup**. That's a zip containing
   `KokoroVoiceover-Setup.exe` — the real, finished, installable app,
   icon and all. Double-click it on any Windows PC to install.

You only need to repeat steps 3–5 if you change the code later — steps
1–2 are one-time setup.
