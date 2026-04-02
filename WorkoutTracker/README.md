# Netid: neilc21
# Name: Neil Chaudhari
# GitHub Repo: https://github.com/NeilChaudhari21/IntroToAi

# Workout Tracker Web App

A modern, client-side web application for tracking workouts with real-time statistics, progress visualization, and persistent data storage using localStorage.

## Overview

The Workout Tracker helps users log exercises, track personal records, monitor training volume, and visualize long-term progress through an interactive chart. All data is stored locally in the browser, ensuring privacy and instant access.

## Files

- **`index.html`** - Main application UI with form inputs, workout log table, and progress chart
- **`styles.css`** - Responsive styling with CSS variables for theming
- **`script.js`** - Core application logic: data management, chart rendering, statistics calculation
- **`README.md`** - This file

## How to Use

1. **Open the Application**: Open `WorkoutTracker/index.html` in any modern web browser
2. **Log an Exercise**: 
   - Select an exercise from the dropdown menu
   - Enter weight (in lbs), number of sets, and reps
   - Select the date of the workout
   - Click "Add Entry" to save
3. **View Your Workouts**: 
   - Scroll down to see all logged workouts in a table format
   - View computed statistics (total volume, personal records, etc.)
4. **Track Progress**: 
   - Check the progress chart below the log
   - The chart displays maximum weight per exercise over time
   - Multiple exercises are shown in different colors

## Features

### Exercise Logging
- Dropdown menu with pre-configured exercises (Bench Press, Squat, Deadlift, Overhead Press, Pull Up, Barbell Row, Leg Press, Lat Pulldown, Dumbbell Curl)
- Input fields for weight, sets, reps, and date
- Simple one-click entry submission

### Workout Log
- Table view showing all logged exercises
- Columns: Date, Exercise, Weight, Sets, Reps, Volume (calculated), Actions
- Remove individual entries with the "Remove" button
- Data sorted by date for easy reference

### Statistics
- **Total Sessions**: Count of all workout entries
- **Total Volume**: Sum of (weight × sets × reps) across all entries
- **PR Weight**: Personal record (highest weight lifted)
- **Max Sets**: Highest set count recorded
- **Max Reps**: Highest rep count recorded

### Progress Chart
- Line chart visualization using Chart.js library
- Each exercise has a unique color
- Shows maximum weight per exercise per date
- Helps identify trends and progression over time
- Responsive design that adapts to screen size

### Data Persistence
- All workouts automatically saved to browser's localStorage
- Data persists across browser sessions
- No login or internet connection required
- Storage key: `workoutTrackerEntries`

### Responsive Design
- Mobile-friendly layout using CSS Grid
- Adapts to desktop, tablet, and phone screens
- Touch-friendly input fields and buttons

## Technical Details

### Data Structure
Each entry is stored as a JSON object with the following properties:
```json
{
  "id": "unique-uuid",
  "name": "Exercise Name",
  "weight": 185,
  "sets": 3,
  "reps": 8,
  "date": "2026-04-02",
  "createdAt": "2026-04-02T15:30:00Z"
}
```

### Storage
- Entries are stored in `localStorage` with the key `workoutTrackerEntries`
- Maximum storage is browser-dependent (typically 5-10MB)
- All data is local to your device

### Chart Library
- Uses Chart.js (loaded via CDN)
- Line chart displaying weight trends per exercise
- Automatic color assignment for different exercises

### Browser Compatibility
- Works on all modern browsers (Chrome, Firefox, Safari, Edge)
- Requires JavaScript enabled
- CSS Grid support needed for responsive layout

## Supported Exercises

The app includes these pre-configured exercises:
- Bench Press
- Squat
- Deadlift
- Overhead Press
- Pull Up
- Barbell Row
- Leg Press
- Lat Pulldown
- Dumbbell Curl

(Additional exercises can be added by editing the `<select>` options in `index.html`)

## Tips for Best Results

1. **Consistent Logging**: Log your workouts immediately after your session for accuracy
2. **Realistic Goals**: Your personal records and statistics are only as good as your data
3. **Progressive Overload**: Use the chart to identify where you can increase weight, sets, or reps
4. **Data Backup**: Periodically take screenshots of your progress chart
5. **Browser Maintenance**: Don't clear browser data unless you want to reset your workouts

## Future Enhancement Ideas

- Add exercise categories (upper body, lower body, cardio)
- Export data as CSV or JSON
- Workout templates for common routines
- Multiple user profiles
- Cloud backup option
- Mobile app version
- Advanced analytics (1RM estimation, volume trends)
- Rest timer between sets
- Exercise notes and form feedback

## Troubleshooting

**"My data disappeared"**
- Check if you cleared browser history/cache
- Data is stored in localStorage - clearing it will erase all workouts
- Use browser DevTools to inspect localStorage if needed

**"Chart is not showing"**
- Ensure you have internet connection (Chart.js loads from CDN)
- Check browser console for JavaScript errors
- Try refreshing the page

**"Can't add entries"**
- Ensure all fields are filled out
- Weight, sets, and reps must be valid positive numbers
- Date must be selected
- JavaScript must be enabled

## License

This is an educational project created as part of academic coursework.

---

*Last Updated: April 2, 2026*
