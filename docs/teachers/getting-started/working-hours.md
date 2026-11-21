---
seo_title: Configure Teacher Working Hours | Yarpad Help Center
description: Learn how teachers configure Working Hours, lesson duration, the first day of the week, and timezone information in Yarpad.
schema_type: TechArticle
---

# Configure Teacher Working Hours

Working Hours configure one daily working window for your account. You select
one start time and one total working duration, along with the lesson duration
and the first day of the week. Availability and booking decisions remain
controlled by Yarpad's backend rules.

## Open Working Hours

Working Hours is available to teachers only.

### From Calendar

1. Open **Calendar**.
2. Select **Working hours**.

This is the exact navigation path: **Calendar → Working hours**.

### During teacher onboarding

1. Complete the **Teacher profile** onboarding step.
2. On the **Working hours** step, select **Continue**.

Working Hours opens as part of the onboarding sequence. After a successful
save, onboarding continues to **Teaching policies**.

### From Schedule Hub

1. Open **Schedule Hub**.
2. Open the schedule menu.
3. Select **Working hours**.

Working Hours opens in a dialog from Schedule Hub.

## Set up Working Hours for the first time

When you create a new configuration, Monday is preselected for **First day of
week**. You can select another weekday before saving.

Complete these steps:

1. Open **Working hours**.
2. Select **Start hour**.
3. Select **Working duration**.
4. Select **Lesson duration**.
5. Review **First day of week** and select another weekday if needed.
6. Select **Save**.

All four fields are required. The form cannot be saved when **Lesson duration**
is longer than **Working duration**.

### Working Hours fields

- **Start hour** — the time your working window begins.
- **Working duration** — the total length of the working window. Available
  values are 2 through 15 hours in one-hour steps.
- **Lesson duration** — the length of a lesson. Available values are 15, 30,
  45, 60, 75, 90, 105, and 120 minutes.
- **First day of week** — the day on which your calendar week begins. Available
  values are Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, and
  Sunday.

Yarpad calculates the end of the working window from **Start hour** and
**Working duration**. The current form uses one start time and one total
working duration; it does not provide separate hours for individual weekdays
or multiple daily intervals.

## Edit existing Working Hours

Reopening Working Hours loads your saved settings. You can edit **Start hour**,
**Working duration**, **Lesson duration**, and **First day of week**.

For an existing configuration, **First day of week** comes from the saved
configuration. A saved value other than Monday is preserved; existing saved
configurations do not automatically default to Monday.

1. Open **Working hours**.
2. Select the field you want to change.
3. Choose the new value.
4. Select **Save**.

The same **Save** action creates a new configuration or updates an existing
one. After a successful save, the form closes. When Working Hours was opened
from Schedule Hub, the calendar reloads after the dialog closes.

## First day of week and calendars

**First day of week** determines where the calendar week begins.

- Teacher Calendar uses the selected day for week display and navigation
  boundaries.
- Scheduling views such as **Recurring Classes** also use backend-provided
  week-start information.
- Changing **First day of week** changes how weeks are displayed and grouped;
  it does not move already booked sessions to different times.

The backend remains authoritative for availability, booking decisions, weekly
policies, and recurrence behavior. A time inside the working window is not
necessarily bookable.

## If the calendar says Working Hours are required

When Working Hours have not been configured, Calendar displays:

> Working hours must be configured before viewing the calendar.

Select **Configure working hours** to open the Working Hours form. Complete
the required fields and select **Save**. After a successful configuration, the
calendar reloads.

## Timezone information

Working Hours uses your configured account timezone. A **Timezone information**
notice may appear when your account timezone differs from your device timezone.
The notice identifies the configured account timezone and the device timezone.

## Troubleshooting

### A required-field message appears

Select values for all four fields:

- **Start hour** must be selected and valid.
- **Working duration** must be selected and valid.
- **Lesson duration** must be selected and valid.
- **First day of week** must be selected.

### Lesson duration exceeds working duration

Choose a shorter **Lesson duration** or a longer **Working duration**. Lesson
duration cannot exceed the total working duration.

### Working Hours are missing from Calendar

Select **Configure working hours**, complete the form, and select **Save**.
The calendar reloads after the configuration is saved successfully.

### Working Hours are still loading

Wait for the Working Hours form to finish loading. If it does not load, close
and reopen Working Hours and try again. If the problem continues, retry later
or contact support with the message shown by Yarpad.

### Saving fails

Check that all required fields are selected, that each value is valid, and that
**Lesson duration** does not exceed **Working duration**. Try saving again. If
the error continues, retry later or contact support with the message shown by
Yarpad.
