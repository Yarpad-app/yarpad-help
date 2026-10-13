---
seo_title: Configure Teacher Working Hours | Yarpad Help Center
description: Learn how to configure teacher Working Hours, lesson durations, booking availability, and timezone settings in Yarpad.
schema_type: TechArticle
---

# Configure Teacher Working Hours

Working Hours define when students can book lessons with you. Yarpad uses one
working window that repeats every day.

## Open Working Hours

You can open Working Hours in any of these ways:

### From Calendar

1. Open the menu.
2. Expand **Calendar**.
3. Select **Working hours**.

### From Schedule Hub

1. Open **Schedule Hub**.
2. Open the schedule menu.
3. Select **Working hours**.

Working Hours opens in a dialog from Schedule Hub. It opens as a full page
from the Calendar menu.

### During teacher onboarding

1. Complete the **Teacher profile** onboarding step.
2. On the **Working hours** step, select **Continue**.

Working Hours opens as part of the onboarding sequence. After a successful
save, onboarding continues to **Teaching policies**.

## Configure Working Hours for the first time

Select values for all three fields:

- **Start hour** — the time your daily working window begins.
- **Working duration** — how long your working window lasts, from 2 to 15
  hours.
- **Lesson duration** — the length of each suggested lesson slot, from 15 to
  120 minutes.

Yarpad calculates the end time automatically by adding the Working duration to
the Start hour. You do not enter the end time separately.

The same working window repeats every day.

### Choose a duration

Working duration is available in one-hour steps from 2 through 15 hours.
Lesson duration is available in 15-minute steps from 15 minutes through 2
hours. Lesson duration cannot be longer than Working duration.

## Edit an existing configuration

When you open an existing configuration, Yarpad pre-fills **Start hour**,
**Working duration**, and **Lesson duration**.

1. Select the field you want to change.
2. Choose a new start time or duration.
3. Select **Save**.

The same form is used to create and edit Working Hours.

## Save or cancel changes

- Select **Save** to validate and store the current Working Hours.
- Select **Cancel** to close Working Hours without saving your changes.

After a successful save, the full page or dialog closes. In Schedule Hub, the
calendar reloads after the dialog closes.

## How Working Hours affect booking availability

Working Hours define the daily window used to create available lesson slots.

- Yarpad creates lesson slots using your selected Lesson duration.
- A lesson slot must fit completely inside the working window.
- A working window can cross midnight. For example, a window that starts at
  22:00 and lasts 3 hours ends at 01:00 the next day.
- **Unavailable Times** remove lesson slots that conflict with them.
- Existing sessions remove lesson slots that conflict with them.

If you have not configured Working Hours, Calendar shows no available lesson
slots and students cannot book an available slot with you.

## Timezone information

Working Hours use your configured teacher timezone. This timezone determines
how your working window and booking availability are interpreted.

If your configured timezone differs from your device timezone, Working Hours
shows a **Timezone information** card with:

- **Your timezone** — the timezone configured for your Yarpad account.
- **Device timezone** — the timezone detected on your device.

Select **Change timezone** on the card to open the timezone settings page.
After changing your timezone, review the displayed Start hour and calculated
working window. If the times are not correct for your new timezone, update and
resave Working Hours.

Changing your timezone does not promise to preserve the same local working
hours. Review your Working Hours after a timezone change whenever your booking
availability needs to remain at specific local times.

## Troubleshooting

### A required-field message appears

Select values for **Start hour**, **Working duration**, and **Lesson duration**.
All three fields are required before Yarpad can save Working Hours.

### Lesson duration exceeds working duration

Choose a shorter Lesson duration or a longer Working duration. A lesson must
fit inside the working window, so Lesson duration cannot be longer than
Working duration.

### Working Hours are missing

Open Working Hours from **Calendar**, **Schedule Hub**, or the onboarding step.
Select Start hour, Working duration, and Lesson duration, then select
**Save**. Until Working Hours are configured, Calendar does not show available
lesson slots for students.

### The timezone is different from the device timezone

Read the **Timezone information** card. If the configured timezone is wrong,
select **Change timezone** and update it. Then review the Working Hours start
and end times and resave Working Hours if necessary.

Do not assume that changing the timezone keeps the same local working window.

### Working Hours are still loading

Wait for the Working Hours form to finish loading. If it does not load, close
and reopen Working Hours and try again.

### Saving fails

Check that all required fields are selected and that Lesson duration does not
exceed Working duration. Try saving again. If the error continues, retry later
or contact support with the message shown by Yarpad.
