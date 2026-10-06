# Tripbox MVP

This document tracks the minimum version of Tripbox needed to validate the core product idea.

## Core Goal

Prove that users want to turn travel screenshots into organized, verified places.

The MVP is complete when a user can:

1. Import a screenshot
2. Detect the travel place
3. Verify the place
4. Confirm it
5. Save it
6. See it inside a destination
7. View it on a map

---

# Phase 1 — Project Setup

## iOS

- [x] Create SwiftUI project
- [x] Add basic app navigation
- [x] Create placeholder Home screen
- [x] Create placeholder Import screen
- [x] Create placeholder Trip screen
- [x] Confirm app builds in simulator

## Backend

- [x] Create FastAPI project
- [x] Add environment configuration
- [x] Add `/health` endpoint
- [x] Add local development setup
- [x] Confirm backend starts successfully

## Connectivity

- [x] Create basic API client in iOS
- [x] Call `/health` from iOS
- [x] Display successful response
- [x] Handle backend connection failure

### Phase 1 Done When

The iOS app can successfully call the FastAPI backend.

---

# Phase 2 — Screenshot Import

- [x] Add `PhotosPicker`
- [x] Allow user to select one image
- [x] Display selected image in the app
- [x] Show loading state while image loads
- [x] Handle image selection failure
- [x] Convert selected image into uploadable data

### Phase 2 Done When

A user can select a screenshot from Photos and preview it inside Tripbox.

---

# Phase 3 — Screenshot Upload

## Backend

- [x] Add `POST /analyze-screenshot`
- [x] Accept multipart image upload
- [x] Validate file type
- [x] Validate file size
- [x] Return temporary mock response

Example:

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

## iOS

- [x] Upload selected image to backend
- [x] Decode response
- [x] Display detected place
- [x] Show loading state
- [x] Show upload error state

### Phase 3 Done When

A screenshot can travel from iPhone → FastAPI → iPhone and return structured JSON.

---

# Phase 4 — AI Place Extraction

## AI Service

- [x] Add multimodal model integration
- [x] Send screenshot to vision model
- [x] Request structured output
- [x] Detect whether screenshot is travel-related
- [x] Extract place name
- [x] Extract city
- [x] Extract country
- [x] Extract category
- [x] Return confidence score if supported
- [x] Validate AI response before returning it

## Handle Edge Cases

- [x] Screenshot contains no travel place
- [x] Screenshot contains multiple places
- [x] Place name is incomplete
- [x] City is missing
- [x] AI returns malformed output
- [x] AI request fails

### Phase 4 Done When

Tripbox can correctly identify the main place in a real travel screenshot.

---

# Phase 5 — Place Verification

## Places Provider

- [ ] Choose initial places provider
- [ ] Add place search service
- [ ] Search using extracted place name and city
- [ ] Retrieve canonical place name
- [ ] Retrieve address
- [ ] Retrieve latitude
- [ ] Retrieve longitude
- [ ] Retrieve provider place ID
- [ ] Retrieve category/type if available

## Matching

- [ ] Match best result
- [ ] Handle zero results
- [ ] Handle multiple likely matches
- [ ] Return verification confidence or status

### Phase 5 Done When

An AI-extracted place can be matched to a real-world location with coordinates.

---

# Phase 6 — Confirmation Flow

Create a confirmation screen showing:

- [ ] Original screenshot
- [ ] Detected place name
- [ ] City
- [ ] Country
- [ ] Category
- [ ] Address
- [ ] Map preview if available

Actions:

- [ ] Confirm
- [ ] Edit
- [ ] Reject
- [ ] Retry search

### Phase 6 Done When

The user can review and approve a detected place before it is saved.

---

# Phase 7 — Database

## Initial Tables

### Users

- [ ] `id`
- [ ] `created_at`

### Trips

- [ ] `id`
- [ ] `user_id`
- [ ] `name`
- [ ] `country`
- [ ] `created_at`

### Places

- [ ] `id`
- [ ] `name`
- [ ] `city`
- [ ] `country`
- [ ] `address`
- [ ] `latitude`
- [ ] `longitude`
- [ ] `category`
- [ ] `provider_place_id`

### Saves

- [ ] `id`
- [ ] `user_id`
- [ ] `trip_id`
- [ ] `place_id`
- [ ] `screenshot_path`
- [ ] `created_at`

## Backend

- [ ] Configure Supabase/PostgreSQL
- [ ] Add database connection
- [ ] Add models
- [ ] Add create save endpoint
- [ ] Add fetch trips endpoint
- [ ] Add fetch places endpoint

### Phase 7 Done When

A confirmed place remains saved after restarting the app.

---

# Phase 8 — Destination Organization

- [ ] Automatically determine destination
- [ ] Create destination/trip if needed
- [ ] Add place to correct trip
- [ ] Avoid obvious duplicate places
- [ ] Display number of saved places per trip

Example:

```text
Japan
18 places

Italy
7 places
```

### Phase 8 Done When

Saved places are automatically grouped into the correct destination.

---

# Phase 9 — Home Screen

The Home screen should include:

- [ ] App title
- [ ] List of trips
- [ ] Destination name
- [ ] Saved place count
- [ ] Import screenshots button
- [ ] Empty state

Example:

```text
Tripbox

Your Trips

Japan
18 saved places

Italy
7 saved places

+ Import Screenshot
```

### Phase 9 Done When

Users can open Tripbox and immediately see their saved destinations.

---

# Phase 10 — Trip Screen

The Trip screen should show:

- [ ] Destination name
- [ ] Saved places
- [ ] Place category
- [ ] City
- [ ] Screenshot thumbnail if useful
- [ ] List / Map toggle
- [ ] Empty state

Potential category filters:

- [ ] Food
- [ ] Cafe
- [ ] Attraction
- [ ] Shopping
- [ ] Hotel
- [ ] Nature
- [ ] Other

### Phase 10 Done When

Users can browse all the places saved for one trip.

---

# Phase 11 — Map View

- [ ] Add MapKit map
- [ ] Plot saved places using coordinates
- [ ] Show map annotations
- [ ] Tap annotation to view place
- [ ] Fit map to saved locations
- [ ] Handle trips with no coordinates

### Phase 11 Done When

All saved places for a trip can be viewed together on a map.

---

# Phase 12 — Batch Import

Only build this after single-image import works reliably.

- [ ] Select multiple screenshots
- [ ] Process screenshots individually
- [ ] Show processing progress
- [ ] Display results together
- [ ] Separate successful and failed detections
- [ ] Allow user to confirm multiple results

Example:

```text
10 screenshots analyzed

✓ Shibuya Sky
✓ Glitch Coffee
✓ Senso-ji
✕ Not travel related
? Could not confidently identify
```

### Phase 12 Done When

A user can import a batch of screenshots without processing them one by one.

---

# MVP Testing

Create a real screenshot test set.

Target at least:

- [ ] 10 TikTok screenshots
- [ ] 10 Instagram screenshots
- [ ] 5 Reddit screenshots
- [ ] 5 Google Maps screenshots
- [ ] 5 travel website screenshots
- [ ] 5 non-travel screenshots

Track:

- correct place
- wrong place
- correct city
- wrong city
- false travel detection
- missed travel detection
- verification success

---

# Initial Quality Targets

These are goals, not blockers.

## Place Detection

Target:

- [ ] 85%+ correct main-place extraction

## Place Verification

Target:

- [ ] 90%+ successful verification when the correct place name is extracted

## UX

Target:

- [ ] User can go from screenshot to saved place in under 20 seconds

## Reliability

Target:

- [ ] No app crash during normal import flow

---

# User Testing

Before adding major new features:

- [ ] Give app to at least 5 users
- [ ] Ask them to use their own travel screenshots
- [ ] Watch without explaining the UI
- [ ] Record where they get confused
- [ ] Record detection failures
- [ ] Ask whether they want to import more screenshots
- [ ] Ask what they expected to happen next

Strong validation signal:

> The user sees the first results and immediately wants to import more screenshots.

---

# Do Not Build Yet

Do not add these until the core MVP has been tested:

- [ ] AI itinerary generation
- [ ] TikTok share extension
- [ ] Instagram share extension
- [ ] automatic photo scanning
- [ ] collaborative trips
- [ ] friend invites
- [ ] subscriptions
- [ ] trip recommendations
- [ ] booking integrations
- [ ] social feed
- [ ] expense splitting
- [ ] flight tracking
- [ ] hotel search

---

# Current Build Order

Work through these before anything else:

```text
1. FastAPI /health
2. iOS calls /health
3. PhotosPicker
4. Display screenshot
5. Upload screenshot
6. Return mocked place JSON
7. Connect vision model
8. Verify place
9. Confirmation screen
10. Save to database
11. Trip list
12. Map
13. Batch import
14. User testing
```

---

# MVP Definition of Done

Tripbox MVP is complete when a new user can:

- select a real travel screenshot
- have Tripbox identify the place
- have the location verified
- confirm the result
- save it
- find it later under the correct destination
- view it on a map

The MVP does not need to plan the trip.

It needs to prove that turning scattered travel screenshots into organized places is valuable.