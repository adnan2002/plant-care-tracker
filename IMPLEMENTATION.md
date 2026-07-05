# Plant Tracker Pro Implementation Plan

## Codebase Analysis

Plant Tracker Pro is a Streamlit application backed by CSV files in `data/`. The app is organized around page modules in `pages_content/` and shared CSV/data logic in `utils/`.

Current capabilities:

- `main.py` configures Streamlit navigation for adding plants, recording care, viewing due care, searching plants, and listing all plants.
- `pages_content/add_plant.py` lets users add a plant, upload one cover photo, and stores the photo path in `data/plants.csv`.
- `utils/add_plant.py` persists new plant rows and initializes care due dates for watering, fertilizing, repotting, and pruning.
- `utils/care.py` computes due dates from fixed plant-level intervals and records completed care in `data/care_log.csv`.
- `pages_content/due_for_care.py` displays past due and upcoming care from `data/due_log.csv`.
- `pages_content/search_plants.py` and `pages_content/all_plants.py` expose simple plant lookup/listing.

Current gaps against the requested requirements:

- Growth measurements over time are not tracked.
- Seasonal care reminders are not generated from plant type.
- Only one cover photo path is stored per plant; there is no photo history/progress log.
- Care schedules are fixed and do not adjust by season.
- Symptom-based problem diagnosis does not exist.
- Plant type is not currently stored, so seasonal reminders and diagnosis rules need either a new `plant_type` column or a derived type field.

## Requirements Mapping

| Requirement | Current Support | Implementation Needed |
| --- | --- | --- |
| Track plant growth measurements over time | Not supported | Add a growth measurements CSV, utility functions, and a Streamlit page/form to log and view measurements. |
| Generate seasonal care reminders based on plant type | Not supported | Add plant type data, seasonal rule definitions, and a reminders page/section. |
| Allow adding photos/file paths to document plant progress | Partially supported | Keep `photo_path` as cover image and add a photo log CSV for multiple progress photos per plant. |
| Adjust care schedules based on seasonal changes | Not supported | Add season-aware schedule multipliers/overrides and apply them when calculating due dates. |
| Diagnose common plant problems based on symptoms | Not supported | Add symptom/rule-based diagnosis utilities and a Streamlit diagnosis page. |

## Data Model Changes

Add these CSV files under `data/`:

### `data/growth_measurements.csv`

Columns:

- `measurement_id`
- `plant_id`
- `date`
- `height_cm`
- `width_cm`
- `leaf_count`
- `notes`

Purpose: store repeated growth observations for a plant over time.

### `data/plant_photos.csv`

Columns:

- `photo_id`
- `plant_id`
- `date`
- `file_path`
- `caption`

Purpose: store multiple progress photo paths per plant while leaving `plants.csv.photo_path` as the cover photo.

### `data/plant_problem_rules.csv`

Columns:

- `rule_id`
- `symptom`
- `problem`
- `recommendation`
- `plant_type`
- `severity`

Purpose: drive symptom-based diagnoses without hard-coding every rule in Streamlit page code.

### Update `data/plants.csv`

Add column:

- `plant_type`

Purpose: support seasonal reminders and plant-specific diagnosis rules. Example values: `Succulent`, `Tropical`, `Flowering`, `Herb`, `Fern`.

## Utility Module Changes

### `utils/load_plants.py`

Add constants, cached dataframes, load functions, and save functions for:

- `GROWTH_MEASUREMENTS_CSV`
- `PLANT_PHOTOS_CSV`
- `PLANT_PROBLEM_RULES_CSV`

Recommended functions:

- `load_growth_measurements()`
- `save_growth_measurements(df)`
- `load_plant_photos()`
- `save_plant_photos(df)`
- `load_problem_rules()`

### `utils/growth.py`

Add growth measurement behavior:

- `record_growth_measurement(plant_id, date, height_cm, width_cm, leaf_count, notes)`
- `get_growth_history(plant_id)`
- `get_growth_summary(plant_id)`

The summary can calculate latest measurement, previous measurement, and changes over time.

### `utils/photos.py`

Add progress photo behavior:

- `add_progress_photo(plant_id, date, file_path, caption)`
- `get_progress_photos(plant_id)`

If uploaded files are accepted through Streamlit, store files under `data/uploads/plants/{plant_id:04d}/progress/` and persist the resulting path in `plant_photos.csv`.

### `utils/seasons.py`

Add season detection and schedule adjustment behavior:

- `get_season(date)`
- `get_seasonal_care_reminders(plant_type, season)`
- `adjust_frequency_for_season(activity, base_value, unit, plant_type, season)`

Initial rule examples:

- Succulents need less watering in winter.
- Tropical plants may need more humidity reminders in winter.
- Flowering plants may need more fertilizing reminders in spring/summer.
- Most plants slow growth in winter, so fertilizing can be reduced.

### `utils/care.py`

Update care due date calculation to apply seasonal adjustment before calculating the next due date.

Recommended integration points:

- In `record_care()`, call `adjust_frequency_for_season()` after `get_activity_schedule()` and before `update_due_log()`.
- In `ensure_due_log_rows()`, apply the same adjustment when creating missing due rows.
- Include `plant_type` when loading/merging plant data for reminders.

### `utils/diagnosis.py`

Add symptom diagnosis behavior:

- `diagnose_plant(symptoms, plant_type=None)`
- Match selected symptoms against `plant_problem_rules.csv`.
- Return likely problems, severity, and recommendations sorted by match count/severity.

## Streamlit Page Changes

### Add `pages_content/growth_tracker.py`

Features:

- Select a plant.
- Enter date, height, width, leaf count, and notes.
- Save to `growth_measurements.csv`.
- Display measurement history sorted by date.
- Optionally display a Streamlit line chart for height/width over time.

### Add `pages_content/progress_photos.py`

Features:

- Select a plant.
- Upload a progress photo or enter an existing file path.
- Add a date and caption.
- Save metadata to `plant_photos.csv`.
- Display previous progress photos for the selected plant.

### Add `pages_content/seasonal_reminders.py`

Features:

- Select a plant or view all plants.
- Determine current season.
- Display seasonal care reminders based on `plant_type`.
- Display adjusted care intervals next to base intervals so users can understand the seasonal change.

### Add `pages_content/diagnose_problems.py`

Features:

- Select a plant or plant type.
- Select symptoms from common options such as yellow leaves, brown tips, wilting, spots, pests, leggy growth, root rot smell, or dry soil.
- Display likely problems and recommendations from `utils/diagnosis.py`.

### Update `pages_content/add_plant.py`

Add a `plant_type` input to the form and pass it into `utils.add_plant.add_plant()`.

### Update `main.py`

Add navigation entries:

- Growth: `growth_tracker.py`, `progress_photos.py`
- Care: `seasonal_reminders.py`, existing `record_care.py`, existing `due_for_care.py`
- Help: `diagnose_problems.py`

## Implementation Order

1. Add the new CSV files with headers and add `plant_type` to `plants.csv`.
2. Extend `utils/load_plants.py` with load/save functions for the new CSV files.
3. Update add-plant flow to capture and persist `plant_type`.
4. Implement growth measurement utilities and the growth tracker page.
5. Implement progress photo utilities and the progress photos page.
6. Implement seasonal utility rules and integrate adjusted intervals into `utils/care.py`.
7. Implement seasonal reminders page.
8. Implement diagnosis rules, diagnosis utilities, and diagnosis page.
9. Update `main.py` navigation.
10. Manually verify adding a plant, logging growth, adding progress photos, viewing adjusted care, and running diagnosis.

## Verification Checklist

- App starts with `streamlit run main.py`.
- Existing plants still load after adding `plant_type`.
- Adding a plant creates due care rows for all care activities.
- Recording care recalculates the next due date using the current seasonal adjustment.
- Growth entries append to `growth_measurements.csv` and display in date order.
- Progress photos append to `plant_photos.csv` and stored paths are displayed.
- Seasonal reminders change based on plant type and season.
- Diagnosis returns useful recommendations for at least the common symptoms in the seed rules.
