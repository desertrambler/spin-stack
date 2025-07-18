# 🎧 SpinStack

**SpinStack** is a web application for vinyl record collectors to catalog, explore, and enjoy their collections — complete with a built-in **Vinyl Roulette** feature to help you pick what to play next.

Built with **Flask**, **HTMX**, and **Umbrella.js**.

---

## 📦 Features

### 🗃️ Vinyl Catalog
- Add, edit, and delete vinyl records in your personal collection
- Store metadata: title, artist, genre, year, label, condition, and album art
- Tag records with custom notes or mood labels
- Search and filter by artist, genre, decade, condition, etc.
- Upload album art manually or fetch from the [Discogs API](https://www.discogs.com/developers/)

### 🎲 Vinyl Roulette
- “Spin the Record” button randomly selects a vinyl from your collection
- Apply filters to narrow spins by:
  - Genre
  - Mood
  - Decade
  - Play count
- Animated spinning record UI (HTMX + CSS)
- “Skip” to spin again, “Why this pick?” optional feature
- Track play counts for roulette results

### 📊 Collection Stats (Stretch)
- Genre and decade distribution charts
- Most played albums and artists
- Average collection condition
- Recently spun records

### 📝 Listening Log (Optional)
- Log listening sessions with date, time, and notes
- View history per record or overall

### 💡 Other Features
- Wishlist for records you want to own
- CSV/JSON import & export
- Optional trade/sell flags for each record
- Responsive dark mode toggle
- Minimalist, keyboard-friendly interface

---
