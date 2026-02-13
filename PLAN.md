# Family Task Manager Plan

## 1) Objective
Build a web-based task manager for a family where members can:
- Create and manage shared tasks.
- Assign tasks to a family member.
- Organize work with subtasks, dependencies, and tags.
- See assigned tasks on Google Calendar.

## 2) Scope (MVP)
### In scope
- Family user accounts with Google OAuth sign-in.
- Task CRUD with:
  - `name` (required)
  - `description` (optional)
  - `created_at` (system-generated)
  - `deadline` (optional)
  - `assignee` (optional, single assignee)
  - `priority` (`P0`, `P1`, `P2`)
  - `status` (`todo`, `in_progress`, `done`)
- Subtasks (parent/child task relationship).
- Task dependencies ("blocked by" relationships).
- Custom tags.
- Task list UI with:
  - Filter by assignee
  - Sort by priority
  - Sort by deadline
- One-way sync of assigned tasks to assignee's Google Calendar.
- Reminders and notifications for upcoming/overdue tasks.

### Out of scope (MVP)
- Native mobile app.
- Offline mode.
- Complex recurrence rules.
- Multi-family tenancy (single family per deployment for now).

## 3) Product Requirements
### Core behavior
- A task can exist without assignee or deadline.
- A task has at most one assignee.
- A task can have many subtasks.
- A task can be blocked by multiple other tasks.
- Blocked tasks should be visually marked and not shown as "ready."
- Users can create and reuse tags across tasks.
- Priority is fixed enum: `P0`, `P1`, `P2`.
- Status is fixed enum: `todo`, `in_progress`, `done`.

### Calendar behavior
- Sync is one-way only: app -> Google Calendar.
- When a task is assigned (or reassigned), create/update a calendar event for that assignee.
- When a task is unassigned, completed, or deleted, remove or update the corresponding event.
- Deadlines are day-level; calendar events should be all-day on the deadline date.
- Calendar event should include task name, description, deadline date, priority, and link back to the task.

### Reminder and notification behavior
- Users receive reminders for upcoming deadlines.
- Users receive notifications for overdue tasks.
- MVP channels: in-app notifications and email notifications.
- Reminder timing should be configurable globally first (for example, 1 day before and day-of).

## 4) Technical Architecture
### Stack
- Backend: FastAPI (Python)
- Frontend: React
- Database: SQLite (MVP), with schema designed so migration to Postgres is straightforward
- Auth: Google OAuth 2.0 / OpenID Connect
- Background jobs: lightweight async worker (e.g., APScheduler/Celery-lite pattern) for calendar sync retries and reminder dispatch

### High-level design
- React SPA consumes REST API from FastAPI.
- FastAPI handles auth, authorization, task logic, and sync orchestration.
- SQLite stores users, tasks, relationships, and calendar sync metadata.
- Sync layer calls Google Calendar API using per-user OAuth tokens (securely stored).
- Notification layer schedules and dispatches reminder jobs and stores delivery status.

## 5) Data Model (Initial)
- `users`
  - `id`, `google_sub`, `email`, `name`, `created_at`
- `tasks`
  - `id`, `name`, `description`, `created_at`, `deadline_date`, `priority`, `status`, `assignee_id`, `parent_task_id`, `created_by`
- `task_dependencies`
  - `task_id`, `blocked_by_task_id`
- `tags`
  - `id`, `name`, `created_by`
- `task_tags`
  - `task_id`, `tag_id`
- `calendar_sync`
  - `task_id`, `user_id`, `google_event_id`, `last_synced_at`, `sync_status`, `sync_error`
- `notifications`
  - `id`, `user_id`, `task_id`, `type`, `channel`, `scheduled_for`, `sent_at`, `delivery_status`, `error`
- `notification_settings`
  - `family_id`, `remind_days_before`, `remind_on_due_day`, `overdue_digest_time`

## 6) API Surface (MVP)
- `POST /auth/google/callback`
- `GET /me`
- `GET /tasks`
  - Query params: `assignee_id`, `sort=priority|deadline`, `status`, `tag`
- `POST /tasks`
- `GET /tasks/{id}`
- `PATCH /tasks/{id}`
- `DELETE /tasks/{id}`
- `POST /tasks/{id}/dependencies`
- `DELETE /tasks/{id}/dependencies/{blocked_by_id}`
- `POST /tasks/{id}/tags/{tag_id}`
- `DELETE /tasks/{id}/tags/{tag_id}`
- `GET /notifications`
- `PATCH /notifications/{id}` (mark read/dismiss)
- `GET /notification-settings`
- `PATCH /notification-settings`

## 7) Frontend UX (MVP)
- Primary page: task list/table with filters and sort controls.
- Task detail drawer/page:
  - Edit task fields
  - Manage subtasks
  - Manage blockers
  - Manage tags
- Create task modal/form.
- Visual indicators:
  - Overdue tasks
  - Blocked tasks
  - Unassigned tasks
- Notification center/inbox for reminders and overdue alerts.

## 8) Security and Reliability Baseline
- Store OAuth tokens encrypted at rest.
- Use server-side sessions or signed JWT with short expiry.
- Enforce family-only access controls on all task queries/mutations.
- Add audit fields (`created_by`, `updated_at`) and server-side validation.
- Retry failed calendar sync operations with backoff; show sync errors in admin/debug view.
- Retry failed notification sends with backoff and idempotency keys.

## 9) Deployment (GCP VM)
### Runtime
- Single GCP VM running:
  - FastAPI app
  - React static build served via Nginx (or CDN + backend on VM)
  - SQLite on persistent disk
- HTTPS via managed cert + reverse proxy.

### DevOps basics
- Docker Compose for reproducible setup.
- `.env`-driven config for OAuth credentials and secrets.
- Daily DB backups from persistent disk snapshots.
- Basic monitoring/logging (system + app logs).
- SMTP provider/API credentials for email notification delivery.

## 10) Milestones
1. Project setup, auth scaffolding, DB schema, migrations.
2. Task CRUD + list filter/sort.
3. Subtasks + blockers + tags.
4. Google Calendar sync flow + retry/error handling.
5. Reminder/notification system (scheduler + in-app + email).
6. UI polish + validation + access control hardening.
7. Deploy to GCP VM and run smoke tests.

## 11) Acceptance Criteria (MVP)
- Family members can sign in with Google and view only family data.
- Users can create, edit, assign, and delete tasks.
- Users can add subtasks, blockers, and tags.
- Task list supports filter by assignee and sort by priority/deadline.
- Assigned tasks appear as all-day events on assignee's Google Calendar and stay in sync after key updates.
- Users receive reminders/notifications for upcoming and overdue tasks.
- App is deployed and accessible over HTTPS on a GCP VM.

## 12) Confirmed Decisions
- Single family deployment (no multi-family in MVP).
- One assignee per task.
- Priority levels: `P0`, `P1`, `P2`.
- Status model: `todo`, `in_progress`, `done`.
- Calendar sync direction: one-way only (app -> Google Calendar).
- Deadline semantics: day-level deadline, mapped to all-day calendar events.
- Reminders/notifications included in MVP.
- Deployment target: single GCP VM is acceptable.


