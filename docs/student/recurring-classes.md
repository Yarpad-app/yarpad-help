---
seo_title: Manage Your Recurring Classes | Yarpad Help Center
description: Learn how to select and remove recurring weekly class times, and understand how Yarpad later attempts to book individual sessions.
schema_type: TechArticle
---

# Manage Your Recurring Classes

Recurring classes let you select fixed weekly class times. A recurring
selection is not a booked session. Yarpad uses your recurring selections to
attempt to book individual sessions automatically.

## Open Recurring Classes

1. Sign in to Yarpad.
2. Open the navigation menu.
3. Expand **Calendar**.
4. Select **Recurring classes**.

## Understand the Weekly Calendar

The weekly calendar shows one reference week for your recurring selections.
It is not a list of booked sessions.

- **Free slots** are intervals that you can select.
- **Planned** represents recurring slots that you have selected.
- Shaded areas are unavailable.

The page does not provide previous-week or next-week navigation. To see
updated availability or selections, wait for the page to refresh after an
action or reopen it later.

## Add a Recurring Class

1. Find a **Free slots** interval.
2. Select the interval you want.
3. Yarpad submits the selection immediately.
4. Wait for the calendar to refresh.
5. Confirm that the interval appears as **Planned**.

There is no separate **Save** button. Selecting an available interval saves
the recurring selection immediately; it does not immediately book a session.

## Automatic Session Booking

Yarpad runs automatic booking daily. It attempts to create individual sessions
from your recurring selections within the teacher's configured booking
horizon. The default horizon is 14 days, but the teacher's policy may change
this period.

Automatic booking is not immediate. Each booking attempt must pass availability,
booking-policy, and balance checks. A recurring selection does not guarantee
that every future session will be booked.

## Session Balance and Allowance

Selecting a recurring slot does not immediately consume allowance. Allowance
is checked when Yarpad attempts to book an individual session.

Insufficient allowance may prevent automatic booking. Monitor **Session
balance** in Yarpad; the recurring page does not display this balance. Future
booking attempts may occur after allowance becomes available, but they are not
guaranteed immediately.

## Remove a Recurring Class

1. Select a **Planned** interval.
2. Review the confirmation dialog.
3. Select **Delete** to remove the recurring slot.
4. Select **Cancel** to keep it unchanged.

Removing a recurring slot stops future automatic bookings based on that
selection. Existing booked sessions remain unchanged. Removing a recurring
slot does not cancel already booked sessions.

## Why Was My Class Not Booked?

An individual session may not be booked for several reasons, including:

- insufficient session balance;
- teacher unavailable time;
- an existing session conflict;
- teacher booking policies;
- booking horizon restrictions; or
- another applicable scheduling restriction.

The recurring page does not promise a detailed history of automatic-booking
failures. If a session is not booked, check your **Session balance** and the
relevant class and scheduling details before trying again later.

## Troubleshooting

### “Recurring classes are not configured.”

The recurring-class schedule is not configured for your account or teacher
relationship. Contact your teacher if you expect recurring classes to be
available and this message continues.

### “Recurring classes could not be loaded.”

Yarpad could not load the recurring-class calendar. Select **Retry** and wait
for the calendar to load again. If the problem continues, try opening the
page again later.

### No available time slots are shown

Only intervals provided as available by Yarpad can be selected. If there are
no **Free slots**, there is currently no available recurring interval shown on
the reference week. Check again later if your teacher's availability changes.

### I selected a recurring slot, but no session is booked

Selecting a recurring slot creates a recurring selection, not an immediate
booked session. Automatic booking runs daily and only creates a session when
the availability, booking-policy, and balance checks allow it. The configured
booking horizon and other scheduling restrictions can also affect which
individual sessions are attempted.
