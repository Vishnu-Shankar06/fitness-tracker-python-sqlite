# 🏋️‍♂️ NexusFit CLI: Relational Backend Architecture

> 📜 **Note:** This is the scaled backend version of my application. To see the original MVP built purely with Python dictionaries and JSON, [click here] https://github.com/Vishnu-Shankar06/fitness-tracker-python.

> **Local Backend System & CLI Application** for Comprehensive Workout Tracking

An advanced, object-oriented Python command-line application that provides daily workout tracking, weekly goal management, and dynamic motivational feedback. This system utilizes a **local SQLite relational database** to ensure robust data persistence, referential integrity, and scalable architecture.

---

## 🚀 System Highlights & Core Logic

Unlike basic flat-file scripts, this application is engineered with a focus on database integrity and complex state management:

* **Relational Data Persistence:** Replaced volatile dictionary/JSON storage with a persistent SQLite database (`fitness.db`).
* **Object-Oriented Programming (OOP):** Strict separation of concerns between database operations (`Database` class) and application business logic (`FitnessTracker` class).
* **Smart Streak Algorithm:** Employs advanced `datetime` and `timedelta` calculations to track missed days. If a user misses a scheduled workout day, the system automatically detects the gap and resets the streak, enforcing actual discipline.
* **ISO Calendar Integration:** Utilizes Python's `isocalendar()` to dynamically track weekly goals, allowing the system to reset weekly progress accurately regardless of when the user starts.

---

## 🏗️ Database Architecture & Schema

The application automatically provisions a relational database with foreign key constraints to maintain data integrity between user profiles and their historical logs.

### Entity-Relationship Model

#### 1. `users` Table (Profile & State)
Maintains user configuration and current streak states.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier |
| `name` | TEXT | UNIQUE, NOT NULL | User's display name |
| `workout_days` | TEXT | | Comma-separated scheduled days |
| `workout_time` | TEXT | | Target daily workout time |
| `daily_streak` | INTEGER | DEFAULT 0 | Current consecutive active days |
| `weekly_streak` | INTEGER | DEFAULT 0 | Weeks where all goals were met |
| `last_workout_date`| TEXT | | ISO-8601 Date string (YYYY-MM-DD)|

#### 2. `workouts` Table (Activity Log)
Stores chronological logs of all physical activity, tied to the user via a Foreign Key.

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique log identifier |
| `user_id` | INTEGER | FOREIGN KEY (`users.id`) | Relational link to User |
| `date` | TEXT | | ISO-8601 execution date |
| `workout_name` | TEXT | | Type of routine (e.g., Push, Pull) |
| `reps_duration`| TEXT | | Sets/Reps or time duration |

### 🔍 SQL Initialization Example
```sql
-- Schema Generation generated natively via database.py
CREATE TABLE IF NOT EXISTS workouts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date TEXT,
    workout_name TEXT,
    reps_duration TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)            
);
```

---

## 💻 Technical Stack & Dependencies

This system was deliberately built using **Zero External Dependencies** to demonstrate mastery of Python's Standard Library.

* **Language:** Python 3.x
* **Database:** SQLite3 (Native)
* **Standard Libraries Used:** `sqlite3`, `json`, `os`, `random`, `datetime`

---

## 📂 Project Structure

```bash
workout-tracker-sql/
│
├── database.py          # SQLite connection, schema creation, and CRUD operations
├── main.py              # CLI UI, business logic, and datetime calculations
├── quotes.json          # Decoupled dataset of 70+ motivational quotes
├── .gitignore           # Excludes Python cache and local .db files
└── README.md            # System documentation
```

---

## 📊 Sample Execution & UI

The application features a clean, responsive terminal UI that dynamically reacts to database states.

```text
=== 🏋️ Fitness Tracker Console ===
Enter your name: Vishnu Shankar
Welcome Back, Vishnu Shankar

✨ Motivation: "Discipline equals freedom. - Jocko Willink"

1. 🏋️ Log Workout
2. 📊 View Stats
3. ⚙️ Update Schedule
4. 🚪 Exit

Action: 2

=========================
STATISTICS FOR VISHNU SHANKAR
Current Streak: 5 Days
Weekly Streak: 2 Weeks
Total Workouts: 14
Weekly Goal:   |████████--| 80% (4/5)
=========================
View history? (y/n): y
• 2026-03-08: Bench Press - 4 sets/80kg
• 2026-03-09: Squats - 5 sets/100kg
```

---

## 📦 Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Vishnu-Shankar06/fitness-tracker-python-sqlite.git
   ```
2. **Navigate to the directory:**
   ```bash
   cd workout-tracker-sql
   ```
3. **Execute the application:**
   *Note: On the first run, `database.py` will automatically generate the local `fitness.db` file and instantiate the required schema.*
   ```bash
   python main.py
   ```

---

## 🔮 Future Development Roadmap

While currently a fully functional CLI tool, the architecture is designed to support future scaling:
1. **API Integration:** Wrapping `database.py` with FastAPI or Flask to serve data to a web frontend.
2. **Data Export:** Adding functionality to export the `workouts` table to CSV using the `csv` module for external analysis.
3. **Authentication:** Implementing secure password hashing using `bcrypt` for user profiles.

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.