---
seo_title: Manage Teacher Unavailable Times | Yarpad Help Center
description: Learn how teachers add, edit, and remove unavailable periods and control when students can book lessons.
schema_type: TechArticle
---

# Manage Teacher Unavailable Times

Use Unavailable Times to block periods when students should not book lessons.
Unavailable periods appear as blocked regions in Schedule Hub and remove
conflicting booking availability.

## Open Unavailable times

1. Open the menu.
2. Expand **Calendar**.
3. Select **Unavailable times**.

The list shows your existing unavailable periods. If you have not added any,
the page shows **No unavailable times**.

Each entry can show its date, time range, reason, period type, and whether the
reason is visible to students.

## Add an unavailable period

1. On the **Unavailable times** page, select the **Add** icon.
2. Complete the form fields.
3. Select **Save**.

The form opens in a dialog. After a successful save, the dialog closes and the
list reloads.

## Form fields

### Date

Select the date for the unavailable period. For a recurring period, this date
also determines when the recurrence starts. For an **Every week** period, the
selected date determines the weekday that repeats.

### Start time

Select the time when the unavailable period begins.

### End time

Select the time when the unavailable period ends. For a timed period, the End
time must be later than the Start time on the same day.

### Period type

Choose one of the three available period types:

- **Every day** — repeats the unavailable period every day.
- **Every week** — repeats the unavailable period every week on the weekday
  of the selected Date.
- **Specific date** — applies the unavailable period only to the selected
  date.

### Reason

Enter an explanation for the unavailable period. The reason helps you
identify the entry in the list and calendar.

### Reason (visible to students)

Enable this option when students should be able to see the Reason. Leave it
disabled when the reason should remain visible only to you.

### Whole day (24 hours)

Enable **Whole day (24 hours)** to block the entire selected local calendar
day. Yarpad treats a whole-day period as starting at midnight and ending at
the next local midnight. It is not a shorter timed period.

## View and edit an existing period

1. Open **Calendar → Unavailable times**.
2. Select an existing entry.
3. Change its Date, Start time, End time, Period type, Reason, visibility, or
   whole-day setting.
4. Select **Save**.

The same dialog is used to add and edit entries. When you edit a recurring
entry, the change applies to the recurring series. You cannot edit one
individual occurrence from this form.

## Delete an unavailable period

1. On the **Unavailable times** page, select the delete icon for an entry.
2. In the confirmation dialog, select **Remove**.

Select **Cancel** in the confirmation dialog to keep the entry.

Deleting a recurring entry removes its recurring series. You cannot delete one
individual occurrence from this form.

## Save or cancel changes

- Select **Save** in the form to validate and store a new or edited period.
- Select **Cancel** in the form to close it without saving changes.
- Select **Cancel** in the delete confirmation to keep the selected entry.

After a successful save or deletion, the unavailable-times list reloads.

## How unavailable periods affect scheduling

Unavailable periods block overlapping student booking slots. A lesson slot
that overlaps an unavailable period is not available for student booking.

- Existing scheduled lessons are not cancelled or changed when you add an
  unavailable period.
- Unavailable regions appear in Schedule Hub as blocked calendar regions.
- Refresh the calendar or reopen the relevant calendar view after adding,
  editing, or deleting a period if the change is not shown immediately.

The reason is separate from the blocked time. Showing a reason to students
does not change which booking slots are blocked.

## Timezone information

Unavailable periods use your configured teacher timezone. The list converts
period dates and times for that timezone.

When your configured timezone differs from your device timezone, the page shows
a **Timezone information** card with:

- **Your timezone** — the timezone configured for your Yarpad account.
- **Device timezone** — the timezone detected on your device.

Select **Change timezone** on the card to open the timezone settings page.
After changing the configured timezone, review your unavailable periods. Their
displayed dates, times, and recurring weekday can depend on the configured
timezone, so update and resave an entry when its local schedule needs to be
adjusted.

## Troubleshooting

### A required-field message appears

Select values for **Date**, **Start time**, **End time**, and **Period type**,
and enter a **Reason**. These fields are required before the form can be
saved.

### End time is not valid

Make sure End time is later than Start time. Timed unavailable periods must
start and end on the same local day and cannot cross midnight. To block the
whole day, enable **Whole day (24 hours)** instead.

### The whole-day period is not what you expected

Check the selected Date and configured timezone. A whole-day period covers
that local calendar day from midnight to the next local midnight. Review the
entry after changing your timezone.

### The change is not visible in Schedule Hub

Wait for the save or deletion to complete, then refresh the calendar or reopen
the relevant calendar view. Schedule Hub may need to request fresh availability
before the blocked region appears.

### Unavailable times are still loading

Wait for the list or form to finish loading. If it does not load, close and
reopen **Calendar → Unavailable times** and try again.

### Saving or deleting fails

Check the required fields and the Start time and End time order, then try
again. If the error continues, retry later or contact support with the message
shown by Yarpad.
