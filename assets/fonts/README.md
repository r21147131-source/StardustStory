Optional: drop Cinzel-*.ttf / Inter-*.ttf here if this environment cannot
reach Google Fonts at render time (this sandbox's egress policy blocks
fonts.google.com — see build/decisions.md). If empty, pipeline/look.py
falls back to a system Inter build and a bundled serif for Cinzel, and
logs the substitution.
