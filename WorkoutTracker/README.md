# Netid: neilc21
# Name: Neil Chaudhari
# GitHub Repo: https://github.com/NeilChaudhari21/IntroToAi

# Workout Tracker Web App

Advanced client-side web app to log workouts with session-based tracking, live timers, rest intervals, and AI recommendations based on historical performance.

## Files
- `index.html` - app UI with session controls, active workout panel, and day-grouped log
- `styles.css` - styling for sessions, timers, day grouping, and responsive layout
- `script.js` - session management, localStorage, timers, recommendations, and chart rendering

## Run
1. Open `WorkoutTracker/index.html` in a browser.
2. Click "Start Workout" to begin a session.
3. Add sets and track your workout with live timers.

## New Features (v2.0)

### Workout Sessions
- **Start/End Workout**: Begin and complete a full workout session with automatic timestamping
- **Live Workout Timer**: Displays elapsed time during active sessions (HH:MM:SS format)
- **Session Status**: Shows ongoing/completed status for each workout

### Exercise Tracking
- Add multiple sets within a single session
- Input: Exercise, Weight, Sets, Reps, Rest duration
- Each set captures volume calculation and rest preferences
- Remove individual sets before ending workout

### Rest Timer
- **Configurable Rest Intervals**: Set rest time per exercise (default 60s, range 15-120s)
- **Countdown Display**: Visual timer showing remaining rest in MM:SS format
- **Alert Notification**: Audio alert or message when rest period completes
- **Form Locking**: Prevents new set entry while rest timer is active

### Recommendations Engine
- Analyzes historical session data by exercise
- **Progressive Overload Algorithm**:
  - If last session ≥ target reps → suggest +5 lbs
  - If last session < target reps → suggest same or -2.5 lbs
- Displays: Recommended weight, sets×reps, session history, average volume
- Updates dynamically as you add sets in current session

### Day-Based Grouping
- Workout log organized by date
- **Collapsible Day Cards**: Expand/collapse to view sessions by day
- Each day shows total sets count
- Session cards display:
  - Start/end times
  - Completed/ongoing status
  - All sets with exercise, weight, sets, reps, and volume

### Data Persistence
- **Dual Storage Model**:
  - Session format: Full workout objects with metadata in `workoutTrackerSessions`
  - Legacy format: Flat entries in `workoutTrackerEntries` (backward compatible)
- Data persists across browser sessions

### Progress Chart
- Line chart showing max weight per exercise per date
- Continues to track long-term progress
- Updated with each workout completion

### Manual Entry (Legacy)
- Still supports manual single-entry logging for outside-session data
- Backward compatible with existing data

## Statistics
Real-time stats updated after each session:
- Total Entries (all-time sessions)
- Total Volume (sum of weight × sets × reps)
- Personal Record (max weight lifted)
- Max Sets (highest set count in single exercise)
- Max Reps (highest rep count in single exercise)

## Data Model

### Session Object
```json
{
  "id": "uuid",
  "date": "YYYY-MM-DD",
  "startTime": "ISO-8601",
  "endTime": "ISO-8601 or null",
  "setEntries": [
    {
      "id": "uuid",
      "exercise": "Bench Press",
      "weight": 185,
      "sets": 3,
      "reps": 8,
      "restSec": 60,
      "elapsedSec": 0,
      "volume": 4440
    }
  ],
  "status": "completed|ongoing",
  "notes": ""
}
```

## Recommendation Algorithm Details
Tracks per-exercise:
1. **Max Weight**: Highest weight ever lifted
2. **Average Sets/Reps**: Baseline for target
3. **Last Performance**: Most recent set results

Suggests progressive increases when:
- Recent reps ≥ target reps → Add 5 lbs
- Recent reps < target - 2 → Subtract 2.5 lbs (optional deload)
- Otherwise → Maintain current weight

## Browser Storage Keys
- `workoutTrackerSessions` - Array of session objects (new)
- `workoutTrackerEntries` - Array of legacy entry objects (backward compat)

## Future Enhancements
1. Backend database for multi-device sync
2. Form validation (weight/sets/reps within realistic ranges)
3. Edit completed sessions
4. Advanced recommendation algorithms (1RM estimation, periodization)
5. Export data as CSV
6. Multiple user profiles
7. Workout templates
8. Body weight exercises and calisthenics tracking
