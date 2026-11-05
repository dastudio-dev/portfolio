---
name: portfolio-schedule
description: Plan and schedule Instagram Reels of DAStudio (perfil dastudioweb) in Metricool, uploading the mp4s from proyectos/*/renders/ to a public GitHub release. Use when asked to plan, schedule, or publish reels/posts for the month, or to check the content calendar.
---

# Portfolio schedule (Metricool + GitHub release)

Monthly flow to schedule the reels made with the `portfolio-reel` skill. It replaces
Ootto (its subscription is not needed): only Claude, GitHub and Metricool (free plan).

## Fixed data (verified 2026-11-04)
- Metricool connector: "Metricool Social Media Management" (`https://ai.metricool.com/mcp`).
  Tools are deferred: load them with ToolSearch first
  (`getBrandSettings`, `getScheduledPosts`, `createScheduledPost`, `updateScheduledPost`,
  `getBestTimeToPostByNetwork`, analytics tools).
- Brand `blogId` = `6145172`, Instagram = `dastudioweb`, timezone `America/Argentina/Buenos_Aires`.
  Always call `getBrandSettings` first and confirm the Instagram handle is still `dastudioweb`
  (it once pointed to another profile). If it differs, stop and tell Diego to relink it in Metricool.
- Free plan: **20 posts/month** (confirmed by Diego 2026-11-04; Metricool's help center says 20, some
  blogs say 30/50 and are wrong). Counted per calendar month. Before scheduling, count what is already
  scheduled for that month with `getScheduledPosts` and never plan more than 20. Google Drive integration
  is Premium: do NOT rely on it.
- Default cadence: Mon/Wed/Fri at 10:00 plus Sundays at 10:00 (best hour from `getBestTimeToPostByNetwork`;
  re-check each month). 3/week + 4 Sundays ≈ 16 posts in a month, which fits the 20 limit (November 2026 =
  16 scheduled). A month with 5 Sundays or 5 Mon/Wed/Fri weeks can exceed 20: trim the plan.

## Flow
1. **Plan**: pick which projects and in what order; list free dates with `getScheduledPosts`.
2. **Reel + caption**: made with `portfolio-reel`. Each project has
   `proyectos/<name>/renders/<name>_vN.mp4` and `caption.txt` (use the newest version).
3. **Diego approves** the video and caption before anything is uploaded or scheduled.
   Once approved, the final copy (mp4 + `caption.txt`) lives in Google Drive:
   `/mnt/diegosteinberg_google_drive_1790645175/1-Trabajo/reels dastudio/<slug>/`
   (`renders/` is gitignored; nothing is committed). Check it is there before step 4.
4. **Public URL**: the connector only accepts public URLs, not local files. Upload to the
   release `reels-assets` of the portfolio repo:
   ```bash
   gh release upload reels-assets proyectos/<name>/renders/<name>_vN.mp4 --repo diegoastein/portfolio
   ```
   First time: `gh release create reels-assets --prerelease ...`. The repo currently resolves to
   `dastudio-dev/portfolio`, so use the URL that `gh release view reels-assets --json assets` returns.
   Publishing files to a public repo needs Diego's OK; the permission classifier may block
   `gh release create/upload` until he adds a Bash permission rule.
5. **Schedule** with `createScheduledPost`: `blogId` 6145172, `providers: [{"network":"instagram"}]`,
   `instagramData: {"type":"REEL","showReelOnFeed":true}`, `text` = the `caption.txt` verbatim,
   `autoPublish: true`, media = release URL. For the first post of a new setup, create it with
   `draft: true` to check Metricool reads the video (it copies it to `static.metricool.com`),
   then `updateScheduledPost` with `draft: false` (the post id changes, the uuid does not).
6. **Verify** with `getScheduledPosts` for the whole range and report dates, titles and plannerUrl.
7. **Metrics** the next month with `getAnalyticsDataByMetrics` to adjust topics and hours.

## Cleanup (Diego's rule, 2026-11-04)
- **GitHub release `reels-assets`: delete its assets on the LAST DAY of every month** (after that day's
  post is published). Metricool already copied each video to its own storage, so the release is only a
  temporary host. Check first that nothing scheduled for the next days still points to a release URL that
  Metricool has not copied (`getScheduledPosts` shows `static.metricool.com` URLs once copied).
  ```bash
  gh release view reels-assets --repo diegoastein/portfolio --json assets --jq '.assets[].name'   # look first
  gh release delete-asset reels-assets <file.mp4> --repo diegoastein/portfolio -y                  # one by one
  ```
  Deleting is irreversible: list the assets to Diego and get his OK in that session before removing.
- **Google Drive (`reels dastudio`): only APPROVED versions stay, and they are never deleted.** When a
  video is replaced by a new approved version, the old (non-approved) file is deleted from Drive
  (`<slug>/` keeps just the current mp4 + `caption.txt`). Diego's rule, 2026-11-04.
- A one-time reminder (scheduled task `limpiar-release-reels-fin-de-mes`) fires on 2026-11-30 20:00; at
  each month end create the next one (`create_scheduled_task`, `fireAt` = last day of the month, 20:00 -03:00).
- When a published/scheduled video is replaced (new render), upload the new file with a new name
  (`<slug>_v2.mp4`), then `updateScheduledPost` with the new URL; keep the same date.

## Rules
- Never schedule without Diego approving the reel and caption (new content); never paraphrase a caption.
- Keep the brand rules of the repo CLAUDE.md (marca neutra DAStudio, no exposed domains).
- Dates cannot be in the past. Times are local Buenos Aires.
- Not verified: whether Metricool retries a failed auto-publish; check the calendar the day of the first post.

## Limits
- 3 posts/week needs ~12 pieces/month; if there are fewer reels, space them out or alternate
  with image/carousel posts made from `img/` (real screenshots only).
- Reel audio is baked into the video; Instagram library audio (`audioConfiguration`) only works
  on business accounts linked to a Facebook Page.
