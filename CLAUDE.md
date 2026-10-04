# Tripbox

Tripbox is an iOS-first travel app that turns travel screenshots into organized places and trips.

The main goal is to make saving travel inspiration effortless.

## Product Goal

The core user flow is:

1. User imports a travel screenshot
2. App sends the screenshot to the backend
3. AI extracts place information
4. The place is verified using a places provider
5. User confirms the result
6. The place is saved under the correct destination
7. Saved places can be viewed in a list and on a map

The MVP should stay focused on this flow.

Do not expand scope unless explicitly requested.

---

## MVP Priorities

Build in this order:

1. SwiftUI app setup
2. FastAPI backend setup
3. iOS to backend connectivity
4. Screenshot selection with PhotosPicker
5. Screenshot upload
6. AI place extraction
7. Place verification
8. Place confirmation UI
9. Database persistence
10. Trip and destination organization
11. Map view
12. Batch screenshot import

---

## Out of Scope for MVP

Do not implement these unless explicitly requested:

- AI itinerary generation
- collaborative trips
- flight booking
- hotel booking
- restaurant reservations
- expense tracking
- subscriptions
- social features
- automatic background screenshot scanning
- TikTok integration
- Instagram integration
- complex AI agents
- LangGraph workflows
- recommendation engines

The first version should prove that users want travel screenshots automatically turned into organized places.

---

## Tech Stack

### iOS

- Swift
- SwiftUI
- PhotosPicker
- MapKit

### Backend

- Python
- FastAPI

### Database

- PostgreSQL
- Supabase

### AI

Use a multimodal vision model to understand screenshots and return structured place information.

Expected result shape:

```json
{
  "travel_related": true,
  "place_name": "Shibuya Sky",
  "city": "Tokyo",
  "country": "Japan",
  "category": "Attraction",
  "confidence": 0.94
}
```

### Place Verification

Use a places provider to verify extracted locations.

Verified place data should include when available:

- canonical place name
- address
- city
- country
- latitude
- longitude
- category
- provider place ID

Do not blindly trust AI-generated place information.

---

## Core Product Principle

Tripbox should reduce work for the user.

Prefer:

```text
Screenshot
    ↓
Place detected
    ↓
Confirm
    ↓
Saved
```

Avoid:

```text
Screenshot
    ↓
Enter place name
    ↓
Enter city
    ↓
Enter country
    ↓
Choose category
    ↓
Enter address
    ↓
Save
```

The user should mostly confirm information rather than manually enter it.

---

## Project Structure

Prefer a structure similar to:

```text
tripbox/
├── ios/
│   └── Tripbox/
│
├── backend/
│   └── app/
│       ├── main.py
│       ├── routes/
│       ├── models/
│       ├── services/
│       └── core/
│
├── docs/
│
├── README.md
└── CLAUDE.md
```

### Backend Responsibilities

`routes/`

- FastAPI endpoints
- HTTP request and response handling
- minimal business logic

`models/`

- Pydantic request models
- Pydantic response models
- shared data schemas

`services/`

- AI screenshot analysis
- place verification
- database operations
- external API integrations

`core/`

- configuration
- environment variables
- shared utilities

Do not place provider or AI logic directly inside route handlers.

---

## API Conventions

Initial health endpoint:

```http
GET /health
```

Example response:

```json
{
  "status": "ok"
}
```

Screenshot analysis endpoint:

```http
POST /analyze-screenshot
```

The endpoint should accept an image and return structured travel-place information.

Keep API contracts simple and stable.

Use typed request and response models whenever practical.

---

## iOS Guidelines

Use SwiftUI unless there is a strong reason not to.

Prefer:

- small reusable views
- clear state ownership
- simple navigation
- native Apple components
- async/await for network requests

Every user-facing async action should account for:

- loading state
- success state
- error state
- empty state when relevant

Do not overbuild the architecture early.

Use simple patterns until the codebase actually requires additional abstraction.

---

## AI Guidelines

Keep the AI pipeline simple.

For the MVP:

```text
Screenshot
    ↓
Vision model
    ↓
Structured place extraction
    ↓
Places provider
    ↓
Verified result
```

Do not introduce:

- multiple AI agents
- planner/executor loops
- autonomous workflows
- unnecessary retrieval systems
- complex prompt chains

unless there is a demonstrated need.

AI output should be validated before being persisted.

Low-confidence or ambiguous results should be surfaced to the user for confirmation.

---

## Engineering Guidelines

- Prefer simple implementations over clever ones.
- Do not overengineer.
- Make the smallest useful change.
- Keep functions focused and readable.
- Avoid unnecessary dependencies.
- Reuse existing code before introducing new abstractions.
- Do not rewrite unrelated files.
- Do not change architecture without a clear reason.
- Preserve existing behavior unless the task requires changing it.
- Keep secrets in environment variables.
- Never commit API keys or credentials.
- Add comments only when they explain something non-obvious.
- Prefer readable code over excessive comments.

---

## Error Handling

Failures should be handled explicitly.

Examples:

- image upload failure
- invalid screenshot
- non-travel screenshot
- AI extraction failure
- ambiguous place
- places API failure
- network failure
- database failure

Do not silently fail.

User-facing errors should be understandable and actionable.

Backend errors should provide useful logs without exposing secrets.

---

## Testing

Run relevant tests or build checks after meaningful changes.

For backend changes:

- run existing tests
- verify FastAPI starts successfully
- verify affected endpoints manually when appropriate

For iOS changes:

- verify the project builds
- test the affected flow in the simulator when possible

When fixing a bug, add or update a test when practical.

Do not claim a feature works unless it has been reasonably verified.

---

## Git Workflow

Make small, focused commits.

Commit after completing a logical feature, fix, or meaningful unit of work.

Good examples:

```text
chore: initialize SwiftUI app
feat: add FastAPI health endpoint
feat: connect iOS app to backend
feat: add screenshot picker
feat: upload screenshot to backend
feat: add screenshot analysis endpoint
feat: verify extracted places
fix: handle failed place detection
docs: update MVP roadmap
```

Guidelines:

- Do not bundle unrelated changes into one commit.
- Use clear commit messages.
- Prefer conventional commit prefixes when appropriate.
- Run relevant checks before committing.
- Do not rewrite, squash, or force-push history unless explicitly requested.
- Do not commit secrets or generated local configuration.
- Push completed work regularly to the remote branch.
- Do not push obviously broken code unless explicitly requested.

Before committing, review the diff and make sure unrelated changes are not included.

---

## Working Style

When implementing a task:

1. Inspect the relevant existing code
2. Understand the smallest change needed
3. Make the change
4. Run relevant checks
5. Fix any issues caused by the change
6. Review the diff
7. Commit the completed logical change
8. Push when appropriate

Avoid changing multiple unrelated systems at once.

If a requested feature would significantly increase scope or conflict with the MVP, call that out before implementing it.

---

## Documentation

Keep documentation updated when behavior or architecture meaningfully changes.

Important files:

- `README.md` — product overview and repository introduction
- `CLAUDE.md` — engineering and agent instructions
- `docs/MVP.md` — implementation roadmap and checklist

Do not duplicate large amounts of documentation across files.

---

## Privacy

Tripbox handles user screenshots, so privacy should be treated as a core product requirement.

For the MVP:

- only process screenshots explicitly selected by the user
- do not scan unrelated photos
- do not retain uploaded images longer than necessary unless the feature requires storage
- avoid collecting unnecessary metadata
- never log sensitive image contents
- clearly separate temporary processing from persistent storage

Future automatic screenshot scanning should not be implemented without explicit product consideration.

---

## MVP Definition of Done

The MVP core flow is complete when a user can:

1. Open Tripbox
2. Select a travel screenshot
3. Upload it successfully
4. Detect the place shown in the screenshot
5. Verify the real-world location
6. Confirm the result
7. Save the place
8. See it under the correct destination
9. See the place plotted on a map

Everything else is secondary until this works reliably.

---

## Product Vision

Tripbox is not meant to generate generic travel recommendations.

Users have already discovered places they care about.

Tripbox turns those discoveries into something useful.

**Discover anywhere. Save to Tripbox. Travel later.**