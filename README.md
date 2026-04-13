# Snake Persistence Task

A PsychoPy-based Snake behavioral task developed in Python to assess behavioral persistence in relation to coping self-efficacy, with synchronized event logging for physiological data collection.

![Snake task screenshot](images/snakegame.png)

## Run (PsychoPy)
1. Keep the folder structure intact (do **not** move `main.py` out of the project folder).
2. Open PsychoPy (Coder).
3. Open `main.py`.
4. Click **Run**.

Controls:
- Arrow keys: move
- `E`: start (instructions / stage screen)
- `Esc`: quit

## Versions and conditions (Neutral / Positive)
At startup, the task asks for:
- `participant_id`
- `version` (A–F)

Each version runs the same set of levels but in a different order. Stages are also labeled as:
- **Neutral**: HUD hidden (no score/time/progress/targets panel)
- **Positive**: HUD shown

Additional Positive-only feedback:
- On collision, a randomized encouraging message appears in a speech-bubble near the snake.
- The snake pauses briefly after a collision so the message can be read (currently 2 seconds).

Note: Participants do not see the Neutral/Positive label on the pre-stage screen (except the “Trial Run” title), but the condition is still saved in the log via the stage name.

## What gets logged
Results are added to `data/snake_data.csv`.

Fields include:
- `participant_id`, `version`, `session_date`, `session_time`, `difficulty`
- `snake_length`, `score`, `score_per_ms`, `hits_per_ms`, `collisions_per_ms`, `target_hit`, `collisions`

## LSL markers (psychophysiology)
The task publishes event markers over Lab Streaming Layer (LSL) so physiological data (ECG/GSR/EEG) can be aligned to gameplay events.

Stream details:
- Name: `SnakeMarkers`
- Type: `Markers`
- 1 channel (string labels)

Marker labels emitted:
- Movement: `keypress_up`, `keypress_down`, `keypress_left`, `keypress_right`
- Reward: `apple_eaten`
- Growth: `snake_growth`
- Collisions: `collision_wall`, `collision_self`
- Feedback (Positive only): `feedback_<message_slug>`
- Stage lifecycle: `stage_start_<stage_slug>`, `stage_complete_<stage_slug>`, `stage_quit_<stage_slug>`

Notes:
- Markers are pushed from inside the stage game loop; failures to push markers will not crash the task.
- For code-only testing, `snake_task/game.py` includes `DEBUG_PRINT_MARKERS` which prints each marker label to the console.

## Easy things to change

### Stages / timing
Edit `snake_task/stages.py`.

`get_stages(version)` defines the stage order for each version A–F. Neutral/Positive HUD visibility is set per stage in this file.

Each stage is a `StageConfig(...)` with:
- `name`: label written to the log
- `duration_sec`: stage duration (seconds)
- `speed_cells_per_sec`: snake speed (higher = faster)
- `no_hit_respawn_sec`: if no target hit occurs for this long, the target respawns

### Core gameplay + visuals
Edit `config.py`.

- `GRID_SIZE`: size of snake segments and movement step (bigger = larger snake/target)
- `START_LENGTH`: starting snake length
- `LENGTH_GAIN_PER_TARGET`: how many segments are added per target
- `LENGTH_LOSS_ON_COLLISION`: how many segments are removed on collision (won’t go below `START_LENGTH`)
- `SCORE_HIT`, `SCORE_COLLISION`: scoring
- `COLLISION_COOLDOWN_SEC`: prevents repeated collision penalties too rapidly

Target size:
- `APPLE_SCALE`: visual scale of the target relative to `GRID_SIZE`

### Play area size (boxed walls)
Edit `config.py`.
- `USE_PLAY_AREA_BOX`: enable/disable the smaller arena
- `PLAY_AREA_CELLS_X`, `PLAY_AREA_CELLS_Y`: arena size in grid cells
- `PLAY_AREA_LINE_WIDTH`, `PLAY_AREA_LINE_COLOR`: wall outline styling

### Sprites (snake + target images)
Edit `config.py`.
- `USE_SPRITES`: enable/disable images (fallback to rectangles if off or missing)
- `SPRITES_DIR`: folder where images live (defaults to `<project>/images`)
- `SPRITE_*` settings: filenames for snake head/body/tail + target

### Pre-stage fixation (+)
Edit `config.py`.
- `SHOW_PRE_STAGE_FIXATION`: show a flashing fixation cross before each stage
- `PRE_STAGE_FIXATION_TOTAL_SEC`: how long it shows
- `PRE_STAGE_FIXATION_FLASH_SEC`: flash rate
- `PRE_STAGE_FIXATION_SIZE_PX`: bigger = larger `+`
- `PRE_STAGE_FIXATION_THICKNESS_PX`: bigger = thicker/brighter-looking lines

## Credits
Snake model assets by Clear_code (CC0): https://opengameart.org/content/snake-game-assets
