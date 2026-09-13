# Data Model

v0.1 tables:

- teams
- players
- heroes
- patches
- matches
- games
- predictions
- experiments

Planned v0.2:

- match_rosters
- player_hero_stats
- team_hero_stats
- hero_pairs
- compositions
- draft_actions
- patch_hero_changes
- source_documents
- research_snapshots

Historical prediction rule:

For a match at time T, only information with timestamp earlier than T may be used.

Never leak future standings, future roster news, future patch results, or post-match draft information into historical predictions.
