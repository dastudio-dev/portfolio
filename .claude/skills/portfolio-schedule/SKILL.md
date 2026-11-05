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
- Free plan: ~50 posts/month. Google Drive integration is Premium: do NOT rely on it.
- Default cadence: 3 posts/week, Mon/Wed/Fri at 10:00 (best hour from `getBestTimeToPostByNetwork`;
  re-check each month).

## Flow
1. **Plan**: pick which projects and in what order; list free dates with `getScheduledPosts`.
2. **Reel + caption**: made with `portfolio-reel`. Each project has
   `proyectos/<name>/renders/<name>_vN.mp4` and `caption.txt` (use the newest version).
3. **Diego approves** the video and caption before anything is uploaded or scheduled.
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
