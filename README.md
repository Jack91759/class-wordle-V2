# ClassWordle v2 🎓🟩

A full-featured classroom Wordle platform built with Flask.  
Designed for teachers, students, and competitive gameplay with leaderboards, statistics, daily challenges, infinite mode, solution sharing, and live classroom tracking.

---

# 🌐 Live Demo

Try it here:

https://classwordle.pythonanywhere.com/

---

# 📌 Features

## 👨‍🏫 Teacher Features

- Set custom classroom Wordle words
- Monitor all active student games live
- View detailed student statistics
- View student passwords/usernames
- Reset or update student passwords
- Track wins, streaks, and completion rates
- View recent student activity
- Recommended solution analysis system

---

## 👨‍🎓 Student Features

- Student account registration/login
- Classroom Wordle mode
- Daily Wordle mode
- Infinite/random Wordle mode
- Persistent game saves
- Personal statistics tracking
- Win streak tracking
- Leaderboards
- Solution sharing and viewing

---

## 📊 Statistics & Analytics

- Total games played
- Total wins
- Win percentage
- Current streaks
- Average guesses
- Recent activity tracking
- Fastest solves
- Perfect games

---

## 🎮 Game Modes

### 🏫 Classroom Mode

Teachers set a shared word for the entire class.

Students compete against each other using the same puzzle.

---

### 📅 Daily Wordle

A globally shared daily word generated automatically using the current date.

One puzzle per day.

---

### ♾️ Infinite Mode

Unlimited randomly generated Wordle games.

Perfect for practice and competitions.

---

## 🧠 Accurate Wordle Logic

The game includes proper duplicate-letter handling just like the official Wordle game.

Example:

- Correct letters = 🟩
- Present but misplaced = 🟨
- Not in word = ⬛

---

# 🖼️ Screens & Pages

## Main Pages

- `/`
- `/student/login`
- `/student/register`
- `/student/select`
- `/student/game`
- `/student/daily`
- `/student/infinite`
- `/leaderboard`
- `/teacher`
- `/student_search`
- `/classwordle/players`

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Jack91759/class-wordle.git
cd class-wordle
```

---

## 2. Install Dependencies

```bash
pip install flask flask_sqlalchemy sqlalchemy
```

---

## 3. Run the Server

```bash
python flask_app.py
```

Server runs on:

```text
http://127.0.0.1:5000
```

---

# 🛠️ Technologies Used

- Python
- Flask
- SQLAlchemy
- SQLite
- HTML/CSS/JavaScript
- Jinja2 Templates

---

# 📂 Project Structure

```text
class-wordle/
│
├── templates/                 # HTML templates
├── static/                    # CSS / JS / assets
├── flask_app.py               # Main Flask application
├── wordle_classroom.db        # SQLite database
├── README.md
```

---

# 🗄️ Database Models

The project includes several database models:

- `Student`
- `Game`
- `DailyGame`
- `InfiniteGame`
- `DailyWord`
- `TeacherWord`
- `Solution`

---

# 🔐 Authentication

## Teacher Login

Teacher authentication uses a password stored in:

```python
TEACHER_PASSWORD = 'admin123'
```

Change this before deploying publicly.

---

## Student Accounts

Students can:

- Register accounts
- Log in
- Track progress
- Save game history automatically

---

# 📈 Leaderboards

Leaderboards include:

- Highest win rate
- Most wins
- Most games played

Minimum game requirements apply for fairness.

---

# 🔎 Student Search System

Search students by:

- Name
- Username

Includes:

- Recent activity
- Win rates
- Streaks
- Average guesses
- Last played date

---

# 🧩 Solution Sharing System

Players can view community solve paths for words.

Example route:

```text
/solutions/APPLE/daily
```

Includes:

- Recommended solves
- Fastest solutions
- Winning paths
- Guess breakdowns

---

# ⚡ API Endpoints

## Classroom APIs

```text
/api/classwordle/players
/make_guess
/get_game_state
```

---

## Daily APIs

```text
/daily/make_guess
/daily/get_game_state
```

---

## Infinite APIs

```text
/infinite/make_guess
/infinite/get_game_state
```

---

## Utility APIs

```text
/api/random_word
/search_students
/set_word
```

---

# 🎯 Example Use Cases

- Classroom vocabulary practice
- English learning activities
- Friendly classroom competitions
- Coding demonstrations
- Word puzzle communities
- Practice for official Wordle

---

# ⚠️ Important Notes

## Security

This project currently:

- Stores plain student passwords for teacher viewing
- Uses a hardcoded teacher password
- Runs in Flask debug mode by default

Do NOT deploy publicly without improving security.

---

# 🔧 Recommended Improvements

Some good next upgrades:

- Better password security
- Email/password recovery
- Multiplayer classrooms
- Socket-based live updates
- Mobile app support
- Admin dashboards
- Timed competitions
- Achievements/badges
- Custom dictionaries
- Dark mode

---

# 🤝 Contributing

Pull requests are welcome.

1. Fork the repository
2. Create a branch
3. Make changes
4. Submit a pull request

---

# 📜 License

Open-source project.

---

# 🙌 Credits

Inspired by:

- Wordle
- Classroom learning games
- Open-source Flask projects

---

# 📧 Contact

Created by Hack37 Studios

https://hack37studios.pythonanywhere.com/

v1 Project Repository:

https://github.com/Jack91759/class-wordle

v2 Project Repository:

https://github.com/Jack91759/class-wordle-V2
