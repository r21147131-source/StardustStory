# Timberland Story — video production

"How a Poor Russian Boy Created Timberland" — a narrated documentary-style
YouTube video built from the user's own script and voiceover recording.

## Status

Assembly pivoted from a local Remotion render to vidIQ's server-side
`vidiq_compose` tool. This session's network egress policy blocks direct
downloads from arbitrary external hosts (stock footage CDNs, etc.), so a
local Remotion/ffmpeg render couldn't pull in the required B-roll and
AI-generated clips. `vidiq_compose` renders entirely server-side from
hosted URLs, which avoids that constraint.

Because `vidiq_compose` caps output at 240s per call, the ~9:53 video is
split into 3 segments (`production/compose-segments.json`), rendered
separately, then stitched into one final file.

## Files

- `production/script.txt` — full narration script, split by section.
- `production/shot-list.json` — the ~44-shot list with timecodes, source
  type (B-roll vs. AI-generated), source URL, and on-screen duration,
  reconciled to match the voiceover's exact length.
- `production/compose-segments.json` — the shot list split into 3
  sub-240s segments for `vidiq_compose`.
- `public/voiceover.m4a` — the user-provided voiceover recording.

## TMDB

TMDB data is available two ways. Both read the token from the
`TMDB_ACCESS_TOKEN` environment variable (copy `.env.example`; never commit
the real token):

- `.mcp.json` registers the `tmdb` MCP server for Claude Code.
- `node scripts/tmdb.mjs search "Timberland"` / `node scripts/tmdb.mjs get /movie/603`
  for direct API calls.
