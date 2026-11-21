---
seo_title: Manage Your Recurring Classes | Yarpad Help Center
description: Learn how students select and remove recurring classes, view the weekly schedule, and read automatic-booking results in Yarpad.
schema_type: TechArticle
---

# Manage Your Recurring Classes

Recurring classes let you select fixed weekly class times. A recurring
selection is not a booked session. Yarpad uses your recurring selections to
attempt to book individual sessions automatically.

## Open Recurring Classes

Recurring classes are available to signed-in students.

1. Open **Calendar**.
2. Select **Recurring classes**.

The exact navigation path is **Calendar → Recurring classes**.

The page has two tabs:

- **Weekly schedule** — opens by default.
- **Booking report** — shows automatic-booking occurrence records.

## Weekly schedule

The weekly schedule shows a backend-provided reference week for your recurring
selections. It is not a list of booked sessions.

- **Free slots** are available recurring time slots provided by Yarpad.
- **Planned** represents recurring slots that you have selected.
- **Unavailable regions** are times that cannot be selected.

Planned recurring slots are not confirmed booked sessions. The week start and
visible working-hour range come from the backend. There are no previous-week or
next-week controls, and you cannot change lesson duration here.

When you have more than one teacher, Weekly schedule currently has no teacher
selection control. Its calendar configuration uses the first teacher returned
by the backend. This page does not provide separate weekly calendars or promise
combined availability across teachers.

### Add a recurring slot

1. Open **Weekly schedule**.
2. Find a **Free slots** entry.
3. Select the available time.
4. Wait for the schedule to refresh.
5. The selected slot appears as **Planned**.

Selection is saved immediately. There is no separate **Save** button and no
creation confirmation dialog. Which slots are available is determined by the
backend.

### Remove a recurring slot

1. Select a **Planned** slot.
2. Review the confirmation dialog.
3. Select **Delete** to remove it.
4. Select **Cancel** to keep it.

The dialog displays:

> Remove recurring classes

> This recurring classes will be removed. Existing booked Sessions will remain unchanged.

Removing a recurring slot stops that recurring selection. Previously booked
sessions remain unchanged. Removing a recurring slot does not cancel already
booked sessions.

## View Your Booking Report

1. Open **Recurring classes**.
2. Open the **Booking report** tab.

The report loads when you select the tab for the first time. It contains
automatic-booking occurrence records and is read-only. You cannot book, cancel,
reschedule, or retry bookings from this report.

### Understanding report entries

Each entry may include:

- **Teacher** — the teacher associated with the occurrence, when available.
- **Occurrence start** — the occurrence date and time, including the end time
  when available.
- **Status** — the booking outcome returned by the backend.
- **Message** — additional information supplied by the backend, when available.

The report uses these statuses:

- **Not booked** — the occurrence was not booked.
- **Cancelled** — the occurrence is recorded as cancelled.
- **Already booked** — the occurrence is recorded as already booked.

Use the backend-provided **Message** for any additional information. The report
does not provide more detailed explanations than that message.

### Report timezone

The report displays a **Timezone** label. Occurrence times use your configured
student timezone supplied by the backend. Yarpad does not convert these times
again using your browser or device timezone. Numeric UTC offsets are not
necessarily displayed beside individual entries.

### Scrolling and loading more entries

Additional report entries load automatically when you scroll toward the
beginning or end of the report. Loading indicators may appear.

If loading report entries fails, select **Retry** when it is shown. Previously
loaded entries remain available when a subsequent page request fails.

The report does not have a **Load more** button, page-number navigation, manual
sorting, or filters.

The report can contain entries for different teachers, and teacher names appear
when provided. This is separate from Weekly schedule, which has no teacher
selection control and uses the first teacher returned by the backend for its
calendar configuration.

## Automatic session booking

Yarpad runs automatic booking daily. It attempts to create individual sessions
from your recurring selections within the teacher's configured booking
horizon. The default horizon is 14 days, but the teacher's policy may change
this period.

Automatic booking is processed by the backend. It is not immediate: selecting a
recurring slot does not immediately book every future session. Each booking
attempt depends on availability and applicable booking rules, including
booking-policy and balance checks. A recurring selection does not guarantee
that every future session will be booked.

The **Booking report** shows occurrence statuses and backend messages. It does
not provide automatic recovery of failed bookings, immediate retries, or
booking controls.

### Session balance and allowance

Selecting a recurring slot does not immediately consume allowance. Allowance is
checked when Yarpad attempts to book an individual session.

Insufficient allowance may prevent automatic booking. Session balance is
separate from this page; the recurring-classes page does not display or change
that balance. Do not assume that a later booking attempt or recovery will occur
immediately.

## Troubleshooting

### “Recurring classes are not configured.”

Recurring classes are not configured for your account or teacher relationship.
Contact your teacher if you expect recurring classes to be available and this
message continues.

### “Recurring classes could not be loaded.”

Yarpad could not load the Weekly schedule. Select **Retry** and wait for the
calendar to load again. If the problem continues, try opening the page again
later.

### “No booking report entries.”

The Booking report does not currently contain any entries. The report is
read-only; it does not create or retry bookings.

### “Booking report could not be loaded.”

Yarpad could not load the Booking report. Select **Retry** and try again.

### “Previous report entries could not be loaded.”

Yarpad could not load additional entries while you were scrolling toward the
beginning of the report. Select **Retry** when it is shown. Previously loaded
entries remain available.

### “More report entries could not be loaded.”

Yarpad could not load additional entries while you were scrolling toward the
end of the report. Select **Retry** when it is shown. Previously loaded entries
remain available.

### No Free slots are shown

Only slots provided as available by Yarpad can be selected. If there are no
**Free slots**, there is currently no available recurring time shown in the
backend-provided reference week. Availability and booking decisions remain
backend-controlled.
