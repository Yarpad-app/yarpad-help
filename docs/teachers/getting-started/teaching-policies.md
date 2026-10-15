---
seo_title: Configure Teacher Policies | Yarpad Help Center
description: Learn how to configure the booking and cancellation policies that apply to student-initiated sessions in Yarpad.
schema_type: TechArticle
---

# Configure Teacher Policies

Teacher policies define how far in advance students can book or cancel a
session and how many sessions they can book in a week. You can change each
policy's value or turn an individual policy off.

## Open Teaching policies

1. Sign in to Yarpad as a teacher.
2. Open the menu.
3. Expand **Settings**.
4. Select **Teaching policies**.

The **Teaching policies** page shows the policies configured for your teacher
account.

## Review the policy list

Each policy appears in its own card with its title, description, current
status, and an **Edit** action.

- **ON** means the policy is enabled and is enforced for applicable student
  actions.
- **OFF** means the policy is disabled and is not enforced. The policy remains
  in the policy list and can be enabled again later.

## Edit a policy

1. Select **Edit** on the policy you want to change.
2. In the edit panel, review or change **Policy enabled**.
3. Set the policy's value. Duration policies use an amount and a unit such as
   **Hours** or **Days**. The weekly limit uses a whole-number value.
4. Leave **Notify students about changes** off or turn it on as needed.
5. Select **Save**.

Select **Cancel** to close the edit panel without saving your changes.

After a successful save, Yarpad shows **Your policy saved successfully.** and
reloads the policy list.

The **Notify students about changes** option can be changed, but automatic
notifications about policy changes are not currently available. Turning on
this option does not currently send a notification to students.

## Policies currently available

Yarpad currently provides these four policies. The values below are the seeded
defaults for a teacher account; you can change them when you edit a policy.

### Minimum Booking Notice

Default: **24 hours**.

This policy sets how close to the session start a student can book. With the
default, a student can book a session starting at least 24 hours from the
current time. A booking exactly 24 hours before the start is allowed; a
booking made less than 24 hours before the start is rejected by this policy.

### Minimum Cancellation Notice

Default: **3 hours**.

This policy sets how close to the session start a student can cancel. With the
default, a student can cancel through exactly 3 hours before the session
starts. A cancellation made after that cutoff is rejected by this policy.

### Maximum Booking Horizon

Default: **14 days**.

This policy limits how far ahead a student can book. With the default, a
student can book a session up to and including 14 days in advance. A session
scheduled beyond that point is rejected by this policy.

### Weekly Booking Limit

Default: **2 sessions**.

This policy limits the number of countable sessions a student can book during
the teacher's week. With the default, the third countable session is rejected
when the student already has two planned, held, or reserved sessions in that
week.

## How policies affect bookings and cancellations

Enabled policies are enforced for student-initiated actions:

- Student bookings are checked against **Minimum Booking Notice**, **Maximum
  Booking Horizon**, and **Weekly Booking Limit**.
- Student cancellations are checked against **Minimum Cancellation Notice**.

Turning a policy **OFF** removes that policy's enforcement. Other enabled
policies and the normal availability rules still apply.

## How students view your policies

Students can view your policies from your teacher details:

1. The student opens your teacher details.
2. The student selects the **Policies** tab.

The tab shows the policy titles and descriptions provided for your teacher.

## If a value cannot be saved

Policy values are required. Check that the value is present and uses the
format shown by the editor, then select **Save** again. Duration values use
**Hours** or **Days**, while **Weekly Booking Limit** uses a number.
