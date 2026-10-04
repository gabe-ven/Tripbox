# Tripbox

**Turn travel screenshots into organized places and trips.**

Tripbox helps people organize travel inspiration they already save across screenshots, social media, maps, and the web.

Instead of digging through hundreds of screenshots later, users can import them into Tripbox and automatically turn them into structured travel places.

---

## The Problem

People constantly save places they want to visit.

A restaurant from TikTok.  
A cafe from Instagram.  
A hidden beach from Reddit.  
A hotel from a travel blog.  
A photo spot from Google Maps.

The problem is that all of that inspiration ends up scattered across different apps and buried inside the camera roll.

When it is finally time to plan the trip, finding everything again becomes a manual process.

Tripbox is designed to bridge the gap between:

**"I want to remember this place."**

and

**"I am actually going there."**

---

## What Tripbox Does

Tripbox lets users import travel screenshots and automatically:

- identify the place
- determine the city and country
- categorize the location
- verify the real-world place
- organize it by destination
- save the original screenshot
- display saved locations on a map

The goal is to make saving travel inspiration almost effortless.

---

## Core Flow

```text
See a place you like
        ↓
Take a screenshot
        ↓
Import it into Tripbox
        ↓
AI identifies the place
        ↓
Tripbox verifies the location
        ↓
Save it to your trip
        ↓
View everything in one place
```

Example:

```text
Screenshot
    ↓
Shibuya Sky
Tokyo, Japan
Attraction
    ↓
Japan Trip
```

---

## MVP

The first version of Tripbox is intentionally focused.

### Screenshot Import

Users can select travel screenshots directly from their photo library.

### AI Place Detection

Tripbox analyzes screenshots and extracts structured information such as:

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

Extracted locations are verified against a places provider to retrieve accurate information such as:

- official place name
- address
- latitude and longitude
- place category

### Destination Organization

Saved places are automatically grouped by destination.

```text
Japan
├── Tokyo
│   ├── Shibuya Sky
│   ├── Glitch Coffee
│   └── Gyukatsu Motomura
│
├── Kyoto
│   ├── Fushimi Inari
│   └── Kiyomizu-dera
│
└── Osaka
    └── Dotonbori
```

### Map View

Users can view their saved locations visually on a map.

---

## MVP Scope

The initial product will include:

- screenshot selection
- screenshot upload
- travel-content detection
- place extraction
- place verification
- place confirmation
- destination grouping
- saved place list
- map view

The first version will **not** include:

- AI itinerary generation
- flight or hotel booking
- social features
- group trips
- expense tracking
- automatic background photo scanning
- subscriptions
- TikTok or Instagram integrations

These may be added later if the core workflow proves useful.

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

- Multimodal vision model for screenshot understanding
- Structured output for place extraction

### Location Data

- Google Places API or another places provider

---

## Project Structure

```text
tripbox/
├── ios/
│   └── Tripbox/
│
├── backend/
│   ├── app/
│   ├── routes/
│   ├── services/
│   └── models/
│
├── docs/
│
└── README.md
```

---

## Initial API

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "ok"
}
```

### Analyze Screenshot

```http
POST /analyze-screenshot
```

Input:

```text
Image file
```

Example response:

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

---

## First Milestone

Tripbox's first major milestone is completing the full flow for a single screenshot:

1. Open the app
2. Select a screenshot
3. Send it to the backend
4. Detect the travel location
5. Verify the place
6. Display the result
7. Save the place
8. View it inside a destination
9. See it plotted on a map

Once this works reliably, the app can expand to batch imports and additional sources.

---

## Future Ideas

Potential future features include:

### Smart Screenshot Import

Detect new screenshots and offer to scan them for travel places.

### Share Extension

Save content directly from:

- TikTok
- Instagram
- Reddit
- Safari
- Google Maps

### Trip Builder

Turn saved places into a day-by-day itinerary based on proximity and travel time.

### Collaborative Trips

Invite friends and combine everyone's saved places.

### Travel Inbox

Use Tripbox as the central place for anything the user wants to remember for a future trip.

---

## Product Principle

Tripbox is not meant to tell users where they should travel.

The user has already discovered places they are interested in.

Tripbox simply makes those discoveries useful.

**Discover anywhere. Save to Tripbox. Travel later.**