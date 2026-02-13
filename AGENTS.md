## Engineering Practices

- Use frameworks and external libraries when they add value; otherwise implement in-codebase
- Write unit tests for backend code.
- Write good e2e tests. They should be easy to read and should test for the core functionality.
- Prefer concise, readable code - iterate to improve clarity
- Backend uses Python with uv for package management

**Preferred workflow:**
1. Create an implementation plan. Ensure all tests pass and everything builds. Wait for approval.
2. Once approved, implement, commit, and create a PR using the `gh` tool (don't ask to create one manually).

**Extremely Important:**
- Develope iteratively. If you are building a UI, take screenshots and reflect on your work. For scripts run them to verify the output. Fix things if you see something wrong.
- Once you are done with code changes. You MUST verify that all the relevant tests pass including the e2e tests. For frontend changes you should take screenshots of the webpage to confirm the behavior. For the backend, spin up the backend and check the API is working as inteded.
- Once you have tested and confirmed everything, you MUST commit the changes and create a PR.

Plan for the app in: PLAN.md
UX mocks in ux-mock/