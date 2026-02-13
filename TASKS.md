# Tasks

## P0 - Must Do Next
- [ ] Replace bootstrap auth with real Google OAuth flow (authorization code + token verification).
- [ ] Add authenticated session handling (secure cookie or JWT strategy) and remove `X-User-Id` header auth.
- [ ] Implement Google Calendar sync worker to create/update/delete assignee all-day events.
- [ ] Persist and refresh Google OAuth tokens securely (encryption at rest).
- [ ] Implement real notification delivery:
  - [ ] Email delivery via SMTP/API provider.
  - [ ] Retry and idempotency for failed sends.
- [ ] Add Alembic migrations for all current models.
- [ ] Add backend automated tests for:
  - [ ] Task CRUD and filter/sort behavior.
  - [ ] Dependencies and blocker state.
  - [ ] Notification scheduling logic.
  - [ ] Family-level access control.

## P1 - Important
- [ ] Add frontend auth flow integration for real Google sign-in.
- [ ] Improve task detail UX for selecting blocker tasks and parent tasks without manual ID entry.
- [ ] Add pagination/search for task list.
- [ ] Add in-app notification center improvements (grouping, unread counts, filters).
- [ ] Add structured error handling and user-facing toasts in frontend.
- [ ] Add API rate limiting and request logging middleware.
- [ ] Add CI pipeline (lint, typecheck, test, build).

## P2 - Nice to Have
- [ ] Add recurring reminders and configurable schedules per user.
- [ ] Add activity/audit timeline per task.
- [ ] Add CSV export for tasks.
- [ ] Add dark/light theme toggle.

## DevOps and Release
- [ ] Finalize production Docker/Compose settings and secrets strategy.
- [ ] Add HTTPS + reverse proxy production docs for GCP VM.
- [ ] Add backup/restore runbook for SQLite data.
- [ ] Add monitoring/alerting baseline (uptime, error rate, worker failures).
- [ ] Run end-to-end smoke test checklist before first release.
