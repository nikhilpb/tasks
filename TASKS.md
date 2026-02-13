# Family Task Manager - Execution Tasks

This task list is designed so each item is a medium-to-large GitHub PR. When Tasks 1-9 are complete, the MVP defined in `PLAN.md` is fully delivered.

## Task Checklist
- [ ] Task 1 - Project foundation, runtime, and schema baseline
- [ ] Task 2 - Google OAuth login and family-scoped authorization
- [ ] Task 3 - Core task CRUD API and validations
- [ ] Task 4 - Task list UI, create/edit flows, and state indicators
- [ ] Task 5 - Subtasks, dependencies, and tags end-to-end
- [ ] Task 6 - Google Calendar sync with retry and sync-state tracking
- [ ] Task 7 - Reminder and notification system (in-app + email)
- [ ] Task 8 - Security, reliability, and quality hardening
- [ ] Task 9 - GCP VM deployment, backups, HTTPS, and smoke validation

## Task 1 - Project foundation, runtime, and schema baseline (Large PR)
### Deliverables
- FastAPI backend scaffolded with `uv` and environment-based configuration.
- React frontend scaffolded and wired to backend API base URL.
- Docker Compose setup for local development (backend, frontend, reverse proxy/app serving).
- Initial DB migrations and models for: `users`, `tasks`, `task_dependencies`, `tags`, `task_tags`, `calendar_sync`, `notifications`, `notification_settings`.
- CI workflow that runs backend unit tests and frontend test suite.

### Verification
- `docker compose up --build` starts the full stack and serves the app.
- `uv run pytest` passes for backend smoke tests.
- Frontend test command (project standard) passes in CI.
- Applying migrations from empty DB creates all required tables.

## Task 2 - Google OAuth login and family-scoped authorization (Large PR)
### Deliverables
- Google OAuth 2.0 / OIDC login flow implemented (`POST /auth/google/callback`, `GET /me`).
- Session/JWT auth with short-lived tokens and secure cookie/session settings.
- Family-only access control middleware/guards applied to all task and notification endpoints.
- Encrypted storage for OAuth refresh/access tokens at rest.
- Backend unit tests for auth success/failure paths and authorization boundaries.
- E2E tests for sign-in and protected-route behavior.

### Verification
- User can sign in with Google and load profile via `GET /me`.
- Unauthenticated requests to protected endpoints are rejected.
- Cross-family/task access attempts are rejected with authorization errors.
- `uv run pytest` includes passing auth + access control tests.
- E2E test for login + protected navigation passes.

## Task 3 - Core task CRUD API and validations (Large PR)
### Deliverables
- Endpoints implemented: `GET /tasks`, `POST /tasks`, `GET /tasks/{id}`, `PATCH /tasks/{id}`, `DELETE /tasks/{id}`.
- Task fields supported per MVP: `name`, `description`, `created_at`, `deadline`, `assignee`, `priority`, `status`, `parent_task_id`, `created_by`.
- Server-side validation for enums, required fields, and date semantics.
- Query support for assignee filtering and sorting by priority/deadline.
- Unit tests for all CRUD operations, filtering, sorting, and validation failures.

### Verification
- API tests cover create/read/update/delete happy paths and invalid payloads.
- `GET /tasks?assignee_id=...&sort=priority` and `sort=deadline` return expected ordering.
- Deleting a task correctly handles dependent records per defined policy.
- `uv run pytest` passes with high coverage for task API modules.

## Task 4 - Task list UI, create/edit flows, and state indicators (Large PR)
### Deliverables
- Task list/table UI with assignee filter and priority/deadline sort controls.
- Create task modal/form and edit flow wired to Task CRUD API.
- Visual states for overdue, blocked, unassigned, and status (`todo`, `in_progress`, `done`).
- Client-side validation aligned with backend rules.
- E2E tests for core user flows: create, edit, assign, status change, delete.

### Verification
- A signed-in user can complete all core task flows from UI without API errors.
- E2E suite verifies filter/sort behavior and state indicators.
- UX implementation matches `ux-mock/` expectations for primary task management interactions.

## Task 5 - Subtasks, dependencies, and tags end-to-end (Large PR)
### Deliverables
- API support for dependency management: `POST /tasks/{id}/dependencies`, `DELETE /tasks/{id}/dependencies/{blocked_by_id}`.
- API support for tag assignment/removal: `POST /tasks/{id}/tags/{tag_id}`, `DELETE /tasks/{id}/tags/{tag_id}`.
- UI for managing subtasks, blockers, and tags in task detail view.
- "Blocked" readiness logic enforced and surfaced in list/detail UI.
- Backend unit tests for dependency graph rules and tag behavior.
- E2E tests for adding/removing subtasks, blockers, and tags.

### Verification
- Blocked tasks are visibly marked and excluded from "ready" state.
- Tag creation/reuse works across multiple tasks.
- Dependency add/remove endpoints and UI actions are covered by passing tests.
- `uv run pytest` and frontend E2E tests pass.

## Task 6 - Google Calendar sync with retry and sync-state tracking (Large PR)
### Deliverables
- One-way sync service (app -> Google Calendar) for assigned tasks.
- Sync triggers on assign, reassign, deadline change, completion/unassign/delete.
- All-day event mapping for day-level deadlines.
- `calendar_sync` state tracking with `sync_status`, `last_synced_at`, `sync_error`.
- Background retry worker with exponential backoff and idempotent sync operations.
- Unit/integration tests for sync event create/update/delete behavior.

### Verification
- Assigning/reassigning tasks creates/updates events in assignee calendar.
- Completing/unassigning/deleting tasks removes or updates calendar events correctly.
- Simulated Google API failures are retried and visible in sync status fields.
- Tests for sync orchestration and retry logic pass reliably.

## Task 7 - Reminder and notification system (in-app + email) (Large PR)
### Deliverables
- Notification settings API: `GET /notification-settings`, `PATCH /notification-settings`.
- Notification inbox API/UI: `GET /notifications`, `PATCH /notifications/{id}`.
- Scheduler for upcoming and overdue reminders using configurable global settings.
- Email notification delivery integration with retry/backoff and delivery status tracking.
- Unit tests for scheduling windows, deduplication/idempotency, and failure handling.
- E2E tests for inbox display and mark read/dismiss flows.

### Verification
- Upcoming and overdue notifications are generated at configured times.
- Notifications are visible in-app and email sends are logged with statuses.
- Failed sends are retried and final state is recorded.
- Backend and E2E notification tests pass.

## Task 8 - Security, reliability, and quality hardening (Medium-Large PR)
### Deliverables
- Audit fields and update timestamps consistently applied.
- Input validation and error contracts standardized across APIs.
- Rate limiting/abuse protections for auth-sensitive endpoints.
- Debug/admin sync error visibility for failed calendar and notification jobs.
- Expanded unit + e2e regression coverage for high-risk paths.
- Developer docs for local run, testing strategy, and operational troubleshooting.

### Verification
- Security and reliability checklist from `PLAN.md` section 8 is satisfied.
- Regression suite passes for auth, task flows, sync, and notifications.
- Known failure states are observable and actionable from app/admin logs/views.

## Task 9 - GCP VM deployment, backups, HTTPS, and smoke validation (Large PR)
### Deliverables
- Production deployment artifacts for single-VM GCP setup.
- Reverse proxy + HTTPS certificate configuration.
- Persistent disk setup for SQLite and automated daily backup routine.
- Environment/secret configuration documented and validated.
- Smoke test script covering login, task CRUD, sync trigger, and notifications.
- Deployment runbook with rollback and incident triage basics.

### Verification
- MVP is live on HTTPS endpoint on GCP VM.
- Backup job executes and restore procedure is documented and tested.
- Smoke tests pass against deployed environment.
- Acceptance criteria in `PLAN.md` section 11 are demonstrably met.

## Project Completion Gate
Project is considered finished when all tasks above are merged and the following are true:
- [ ] All backend unit tests pass in CI.
- [ ] Core end-to-end flows pass in CI.
- [ ] Production deployment is live and smoke-tested.
- [ ] All `PLAN.md` MVP acceptance criteria are checked off with evidence in PRs.
