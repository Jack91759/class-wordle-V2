from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta
from sqlalchemy.orm import joinedload
import random
import string
import hashlib
import json

# List of 5-letter words for infinite mode
WORD_LIST = ["ADIEU",
    "ABOUT", "ABOVE", "ABUSE", "ACTOR", "ACUTE", "ADMIT", "ADOPT", "ADULT", "AFTER", "AGAIN",
    "AGENT", "AGREE", "AHEAD", "ALARM", "ALBUM", "ALERT", "ALIEN", "ALIGN", "ALIKE", "ALIVE",
    "ALLOW", "ALONE", "ALONG", "ALTER", "ANGER", "ANGLE", "ANGRY", "APART", "APPLE", "APPLY",
    "ARENA", "ARGUE", "ARISE", "ARRAY", "ASIDE", "ASSET", "AVOID", "AWAKE", "AWARE", "BADLY",
    "BAKER", "BASES", "BASIC", "BEACH", "BEGAN", "BEGIN", "BEING", "BELOW", "BENCH", "BILLY",
    "BIRTH", "BLACK", "BLAME", "BLANK", "BLIND", "BLOCK", "BLOOD", "BOARD", "BOOST", "BOOTH",
    "BOUND", "BRAIN", "BRAND", "BRAVE", "BREAD", "BREAK", "BREED", "BRIEF", "BRING", "BROAD",
    "BROKE", "BROWN", "BUILD", "BUILT", "BUYER", "CABLE", "CALIF", "CARRY", "CATCH", "CAUSE",
    "CHAIN", "CHAIR", "CHAOS", "CHARM", "CHART", "CHASE", "CHEAP", "CHECK", "CHEST", "CHIEF",
    "CHILD", "CHINA", "CHOSE", "CIVIL", "CLAIM", "CLASS", "CLEAN", "CLEAR", "CLICK", "CLIMB",
    "CLOCK", "CLOSE", "CLOUD", "COACH", "COAST", "COULD", "COUNT", "COURT", "COVER", "CRAFT",
    "CRASH", "CRAZY", "CREAM", "CRIME", "CROSS", "CROWD", "CROWN", "CRUDE", "CURVE", "CYCLE",
    "DAILY", "DANCE", "DATED", "DEALT", "DEATH", "DEBUT", "DELAY", "DEPTH", "DOING", "DOUBT",
    "DOZEN", "DRAFT", "DRAMA", "DRANK", "DREAM", "DRESS", "DRILL", "DRINK", "DRIVE", "DROVE",
    "DYING", "EAGER", "EARLY", "EARTH", "EIGHT", "ELITE", "EMPTY", "ENEMY", "ENJOY", "ENTER",
    "ENTRY", "EQUAL", "ERROR", "EVENT", "EVERY", "EXACT", "EXIST", "EXTRA", "FAITH", "FALSE",
    "FAULT", "FIBER", "FIELD", "FIFTH", "FIFTY", "FIGHT", "FINAL", "FIRST", "FIXED", "FLASH",
    "FLEET", "FLOOR", "FLUID", "FOCUS", "FORCE", "FORTH", "FORTY", "FORUM", "FOUND", "FRAME",
    "FRANK", "FRAUD", "FRESH", "FRONT", "FRUIT", "FULLY", "FUNNY", "GIANT", "GIVEN", "GLASS",
    "GLOBE", "GOING", "GRACE", "GRADE", "GRAND", "GRANT", "GRASS", "GRAVE", "GREAT", "GREEN",
    "GROSS", "GROUP", "GROWN", "GUARD", "GUESS", "GUEST", "GUIDE", "HAPPY", "HARRY", "HEART",
    "HEAVY", "HENCE", "HENRY", "HORSE", "HOTEL", "HOUSE", "HUMAN", "IDEAL", "IMAGE", "INDEX",
    "INNER", "INPUT", "ISSUE", "JAPAN", "JIMMY", "JOINT", "JONES", "JUDGE", "KNOWN", "LABEL",
    "LARGE", "LASER", "LATER", "LAUGH", "LAYER", "LEARN", "LEASE", "LEAST", "LEAVE", "LEGAL",
    "LEVEL", "LEWIS", "LIGHT", "LIMIT", "LINKS", "LIVES", "LOCAL", "LOOSE", "LOWER", "LUCKY",
    "LUNCH", "LYING", "MAGIC", "MAJOR", "MAKER", "MARCH", "MARIA", "MATCH", "MAYBE", "MAYOR",
    "MEANT", "MEDIA", "METAL", "MIGHT", "MINOR", "MINUS", "MIXED", "MODEL", "MONEY", "MONTH",
    "MORAL", "MOTOR", "MOUNT", "MOUSE", "MOUTH", "MOVED", "MOVIE", "MUSIC", "NEEDS", "NEVER",
    "NEWLY", "NIGHT", "NOISE", "NORTH", "NOTED", "NOVEL", "NURSE", "OCCUR", "OCEAN", "OFFER",
    "OFTEN", "ORDER", "OTHER", "OUGHT", "PAINT", "PANEL", "PAPER", "PARTY", "PEACE", "PETER",
    "PHASE", "PHONE", "PHOTO", "PIECE", "PILOT", "PITCH", "PLACE", "PLAIN", "PLANE", "PLANT",
    "PLATE", "POINT", "POUND", "POWER", "PRESS", "PRICE", "PRIDE", "PRIME", "PRINT", "PRIOR",
    "PRIZE", "PROOF", "PROUD", "PROVE", "QUEEN", "QUICK", "QUIET", "QUITE", "RADIO", "RAISE",
    "RANGE", "RAPID", "RATIO", "REACH", "READY", "REALM", "REBEL", "REFER", "RELAX", "REPAY",
    "REPLY", "RIGHT", "RIGID", "RIVAL", "RIVER", "ROBIN", "ROGER", "ROMAN", "ROUGH", "ROUND",
    "ROUTE", "ROYAL", "RURAL", "SCALE", "SCENE", "SCOPE", "SCORE", "SENSE", "SERVE", "SEVEN",
    "SHALL", "SHAPE", "SHARE", "SHARP", "SHEET", "SHELF", "SHELL", "SHIFT", "SHINE", "SHIRT",
    "SHOCK", "SHOOT", "SHORT", "SHOWN", "SIDES", "SIGHT", "SIMON", "SINCE", "SIXTH", "SIXTY",
    "SIZED", "SKILL", "SLEEP", "SLIDE", "SMALL", "SMART", "SMILE", "SMITH", "SMOKE", "SOLID",
    "SOLVE", "SORRY", "SOUND", "SOUTH", "SPACE", "SPARE", "SPEAK", "SPEED", "SPEND", "SPENT",
    "SPLIT", "SPOKE", "SPORT", "SQUAD", "STAFF", "STAGE", "STAKE", "STAND", "START", "STATE",
    "STEAM", "STEEL", "STEEP", "STEER", "STICK", "STILL", "STOCK", "STONE", "STOOD", "STORE",
    "STORM", "STORY", "STRIP", "STUCK", "STUDY", "STUFF", "STYLE", "SUGAR", "SUITE", "SUPER",
    "SWEET", "TABLE", "TAKEN", "TASTE", "TAXES", "TEACH", "TERMS", "TEXAS", "THANK", "THEFT",
    "THEIR", "THEME", "THERE", "THESE", "THICK", "THING", "THINK", "THIRD", "THOSE", "THREE",
    "THREW", "THROW", "THUMB", "TIGHT", "TIMES", "TIRED", "TITLE", "TODAY", "TOPIC", "TOTAL",
    "TOUCH", "TOUGH", "TOWER", "TRACK", "TRADE", "TRAIN", "TREAT", "TREND", "TRIAL", "TRIBE",
    "TRICK", "TRIED", "TRIES", "TRUCK", "TRULY", "TRUNK", "TRUST", "TRUTH", "TWICE", "TWIST",
    "TYLER", "UNCLE", "UNDER", "UNDUE", "UNION", "UNITY", "UNTIL", "UPPER", "UPSET", "URBAN",
    "USAGE", "USUAL", "VALUE", "VIDEO", "VIRUS", "VISIT", "VITAL", "VOCAL", "VOICE", "WASTE",
    "WATCH", "WATER", "WHEEL", "WHERE", "WHICH", "WHILE", "WHITE", "WHOLE",
    "WHOSE", "WOMAN", "WOMEN", "WORLD", "WORRY", "WORSE", "WORST", "WORTH", "WOULD", "WRITE",
    "WRONG", "WROTE", "YOUNG", "YOUTH"
]

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wordle_classroom.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Teacher password (change this!)
TEACHER_PASSWORD = 'admin123'

# Database Models
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    plain_password = db.Column(db.String(120), nullable=True)  # For teacher viewing
    name = db.Column(db.String(100), nullable=False)
    total_games = db.Column(db.Integer, default=0)
    total_wins = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def check_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest() == self.password_hash

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    target_word = db.Column(db.String(5), nullable=False)
    guesses = db.Column(db.Text, nullable=False)  # JSON string
    won = db.Column(db.Boolean, default=False)
    completed = db.Column(db.Boolean, default=False)
    guess_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    game_type = db.Column(db.String(20), default='custom')  # custom, daily, infinite

class TeacherWord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(5), nullable=False)
    set_at = db.Column(db.DateTime, default=datetime.utcnow)

class InfiniteGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    target_word = db.Column(db.String(5), nullable=False)
    guesses = db.Column(db.Text, nullable=False)  # JSON string
    won = db.Column(db.Boolean, default=False)
    completed = db.Column(db.Boolean, default=False)
    guess_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

class DailyWord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(5), nullable=False)
    date = db.Column(db.Date, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class DailyGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    target_word = db.Column(db.String(5), nullable=False)
    date = db.Column(db.Date, nullable=False)
    guesses = db.Column(db.Text, nullable=False)  # JSON string
    won = db.Column(db.Boolean, default=False)
    completed = db.Column(db.Boolean, default=False)
    guess_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

class Solution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    word = db.Column(db.String(5), nullable=False)
    game_type = db.Column(db.String(20), nullable=False)  # daily, infinite
    solution_path = db.Column(db.Text, nullable=False)  # JSON of guess sequence
    guess_count = db.Column(db.Integer, nullable=False)
    won = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('Student', backref='solutions')

# Create tables
with app.app_context():
    db.create_all()

def get_daily_word():
    today = date.today()
    daily_word = DailyWord.query.filter_by(date=today).first()

    if not daily_word:
        # Generate today's word using date as seed for consistency
        random.seed(int(today.strftime('%Y%m%d')))
        word = random.choice(WORD_LIST)
        daily_word = DailyWord(word=word, date=today)
        db.session.add(daily_word)
        db.session.commit()
        # Reset random seed
        random.seed()

    return daily_word.word

@app.route('/')
def home():
    return render_template('index.html')

# ==============================
# CLASSWORDLE PLAYER VIEW ROUTES
# ==============================

@app.route('/classwordle/players')
def classwordle_players():
    # Current teacher word
    current_word = TeacherWord.query.order_by(
        TeacherWord.set_at.desc()
    ).first()

    if not current_word:
        return render_template(
            'classwordle_players.html',
            players=[],
            current_word=None
        )

    # Get all games for current word
    games = (
        Game.query
        .filter_by(target_word=current_word.word)
        .order_by(Game.created_at.desc())
        .all()
    )

    players = []

    for game in games:
        student = Student.query.get(game.student_id)

        guesses = json.loads(game.guesses)

        players.append({
            'student_id': student.id,
            'name': student.name,
            'username': student.username,
            'guess_count': game.guess_count,
            'completed': game.completed,
            'won': game.won,
            'guesses': guesses,
            'created_at': game.created_at
        })

    return render_template(
        'classwordle_players.html',
        players=players,
        current_word=current_word.word
    )


@app.route('/api/classwordle/players')
def api_classwordle_players():
    current_word = TeacherWord.query.order_by(
        TeacherWord.set_at.desc()
    ).first()

    if not current_word:
        return jsonify({
            'success': True,
            'players': [],
            'current_word': None
        })

    games = (
        Game.query
        .filter_by(target_word=current_word.word)
        .all()
    )

    player_data = []

    for game in games:
        student = Student.query.get(game.student_id)

        player_data.append({
            'student_id': student.id,
            'name': student.name,
            'username': student.username,
            'guess_count': game.guess_count,
            'completed': game.completed,
            'won': game.won,
            'guesses': json.loads(game.guesses)
        })

    return jsonify({
        'success': True,
        'current_word': current_word.word,
        'players': player_data
    })


# ==============================
# RANDOM WORD ROUTES
# ==============================

@app.route('/random_word')
def random_word_page():
    word = random.choice(WORD_LIST)

    return render_template(
        'random_word.html',
        word=word
    )


@app.route('/api/random_word')
def api_random_word():
    word = random.choice(WORD_LIST)

    return jsonify({
        'success': True,
        'word': word
    })

#================================
#================================
#================================

@app.route('/student/select')
def student_select():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    student = Student.query.get(session['student_id'])
    if not student:
        return redirect(url_for('student_login'))

    return render_template('student_select.html', student=student)

@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        print(f'\033[31mUser:{username}, Pass:{password}\033[0m')

        student = Student.query.filter_by(username=username).first()
        if student and student.check_password(password):
            session['student_id'] = student.id
            return redirect(url_for('student_select'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('student_login.html')

@app.route('/student/register', methods=['GET', 'POST'])
def student_register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')

        print(f'\033[31mName:{name}, User:{username}, Pass:{password}\033[0m')

        if Student.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
        elif len(password) < 4:
            flash('Password must be at least 4 characters', 'error')
        else:
            student = Student(
                username=username,
                password_hash=Student.hash_password(password),
                plain_password=password,  # Store plain password for teacher access
                name=name
            )
            db.session.add(student)
            db.session.commit()
            session['student_id'] = student.id
            return redirect(url_for('student_select'))

    return render_template('student_register.html')

@app.route('/student/logout')
def student_logout():
    session.pop('student_id', None)
    return redirect(url_for('home'))

@app.route('/student/game')
def student_game():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    student = Student.query.get(session['student_id'])
    if not student:
        return redirect(url_for('student_login'))

    # Get current teacher word
    current_word = TeacherWord.query.order_by(TeacherWord.set_at.desc()).first()
    if not current_word:
        return render_template('student_game.html', student=student, no_word=True)

    # Get or create current game
    current_game = Game.query.filter_by(
        student_id=student.id,
        target_word=current_word.word,
        completed=False
    ).first()

    if not current_game:
        current_game = Game(
            student_id=student.id,
            target_word=current_word.word,
            guesses='[]',
            game_type='custom'
        )
        db.session.add(current_game)
        db.session.commit()

    return render_template('student_game.html', student=student, game=current_game)

@app.route('/student/daily')
def daily_game():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    student = Student.query.get(session['student_id'])
    if not student:
        return redirect(url_for('student_login'))

    today = date.today()
    daily_word = get_daily_word()

    # Get or create current daily game
    current_game = DailyGame.query.filter_by(
        student_id=student.id,
        date=today,
        completed=False
    ).first()

    if not current_game:
        current_game = DailyGame(
            student_id=student.id,
            target_word=daily_word,
            date=today,
            guesses='[]'
        )
        db.session.add(current_game)
        db.session.commit()

    return render_template('daily_game.html', student=student, game=current_game)

@app.route('/teacher')
def teacher():
    if not session.get('teacher_authenticated'):
        return redirect(url_for('teacher_login'))

    # Get current word
    current_word = TeacherWord.query.order_by(TeacherWord.set_at.desc()).first()

    # Get all students with their stats
    students = []
    for student in Student.query.all():
        # Get current game if exists
        current_game = None
        if current_word:
            current_game = Game.query.filter_by(
                student_id=student.id,
                target_word=current_word.word
            ).first()

        students.append({
            'id': student.id,
            'name': student.name,
            'username': student.username,
            'total_games': student.total_games,
            'total_wins': student.total_wins,
            'win_rate': round(student.total_wins / max(student.total_games, 1) * 100, 1),
            'current_game': current_game,
            'plain_password': None  # Will be loaded on demand
        })

    return render_template('teacher.html',
                         current_word=current_word.word if current_word else '',
                         students=students)

@app.route('/teacher/login', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == TEACHER_PASSWORD:
            session['teacher_authenticated'] = True
            return redirect(url_for('teacher'))
        else:
            flash('Invalid password', 'error')
    return render_template('teacher_login.html')

@app.route('/teacher/logout')
def teacher_logout():
    session.pop('teacher_authenticated', None)
    return redirect(url_for('home'))

@app.route('/set_word', methods=['POST'])
def set_word():
    if not session.get('teacher_authenticated'):
        return jsonify({'success': False, 'message': 'Not authorized'})

    word = request.json.get('word', '').upper().strip()
    if len(word) == 5 and word.isalpha():
        teacher_word = TeacherWord(word=word)
        db.session.add(teacher_word)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Word set successfully!'})
    return jsonify({'success': False, 'message': 'Word must be exactly 5 letters!'})

@app.route('/make_guess', methods=['POST'])
def make_guess():
    if 'student_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})

    student = Student.query.get(session['student_id'])
    if not student:
        return jsonify({'success': False, 'message': 'Student not found'})

    guess = request.json.get('guess', '').upper().strip()

    # Get current teacher word
    current_word = TeacherWord.query.order_by(TeacherWord.set_at.desc()).first()
    if not current_word:
        return jsonify({'success': False, 'message': 'No word set by teacher yet!'})

    # Get current game
    current_game = Game.query.filter_by(
        student_id=student.id,
        target_word=current_word.word,
        completed=False
    ).first()

    if not current_game:
        return jsonify({'success': False, 'message': 'No active game found'})

    if current_game.completed:
        return jsonify({'success': False, 'message': 'Game is already over!'})

    if len(guess) != 5 or not guess.isalpha():
        return jsonify({'success': False, 'message': 'Guess must be exactly 5 letters!'})

    # Parse current guesses
    guesses = json.loads(current_game.guesses)

    if len(guesses) >= 6:
        return jsonify({'success': False, 'message': 'No more guesses allowed!'})

    # Check the guess with proper duplicate handling
    target_word = current_game.target_word
    result = ['absent'] * 5

    # Track remaining unmatched letters in target
    target_letters = list(target_word)

    # FIRST PASS: mark correct letters
    for i in range(5):
        if guess[i] == target_word[i]:
            result[i] = 'correct'
            target_letters[i] = None  # Remove matched letter

    # SECOND PASS: mark present letters
    for i in range(5):
        if result[i] == 'correct':
            continue

        if guess[i] in target_letters:
            result[i] = 'present'
            # Remove first occurrence so duplicates are handled correctly
            target_letters[target_letters.index(guess[i])] = None

    # Add guess to game
    guesses.append({
        'word': guess,
        'result': result
    })

    current_game.guesses = json.dumps(guesses)
    current_game.guess_count = len(guesses)

    # Check if won or game over
    won = guess == target_word
    game_over = won or len(guesses) >= 6

    if game_over:
        current_game.completed = True
        current_game.won = won
        current_game.completed_at = datetime.utcnow()

        # Update student stats
        student.total_games += 1
        if won:
            student.total_wins += 1

        # Save solution for sharing
        solution = Solution(
            student_id=student.id,
            word=target_word,
            game_type='custom',
            solution_path=json.dumps([g['word'] for g in guesses]),
            guess_count=len(guesses),
            won=won
        )
        db.session.add(solution)

    db.session.commit()

    # Prepare response with stats for popup
    response_data = {
        'success': True,
        'result': result,
        'game_over': game_over,
        'won': won,
        'target_word': target_word if game_over else None,
        'guess_count': len(guesses)
    }

    if game_over:
        response_data['stats'] = {
            'total_games': student.total_games,
            'total_wins': student.total_wins,
            'win_rate': round(student.total_wins / student.total_games * 100, 1),
            'current_streak': calculate_current_streak(student.id)
        }

    return jsonify(response_data)

@app.route('/daily/make_guess', methods=['POST'])
def make_daily_guess():
    if 'student_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})

    student = Student.query.get(session['student_id'])
    if not student:
        return jsonify({'success': False, 'message': 'Student not found'})

    guess = request.json.get('guess', '').upper().strip()
    today = date.today()

    # Get current daily game
    current_game = DailyGame.query.filter_by(
        student_id=student.id,
        date=today,
        completed=False
    ).first()

    if not current_game:
        return jsonify({'success': False, 'message': 'No active daily game found'})

    if current_game.completed:
        return jsonify({'success': False, 'message': 'Daily game is already complete!'})

    if len(guess) != 5 or not guess.isalpha():
        return jsonify({'success': False, 'message': 'Guess must be exactly 5 letters!'})

    # Parse current guesses
    guesses = json.loads(current_game.guesses)

    if len(guesses) >= 6:
        return jsonify({'success': False, 'message': 'No more guesses allowed!'})

    # Check the guess with proper duplicate handling
    target_word = current_game.target_word
    result = ['absent'] * 5

    # Track remaining unmatched letters in target
    target_letters = list(target_word)

    # FIRST PASS: mark correct letters
    for i in range(5):
        if guess[i] == target_word[i]:
            result[i] = 'correct'
            target_letters[i] = None  # Remove matched letter

    # SECOND PASS: mark present letters
    for i in range(5):
        if result[i] == 'correct':
            continue

        if guess[i] in target_letters:
            result[i] = 'present'
            # Remove first occurrence so duplicates are handled correctly
            target_letters[target_letters.index(guess[i])] = None

    # Add guess to game
    guesses.append({
        'word': guess,
        'result': result
    })

    current_game.guesses = json.dumps(guesses)
    current_game.guess_count = len(guesses)

    # Check if won or game over
    won = guess == target_word
    game_over = won or len(guesses) >= 6

    if game_over:
        current_game.completed = True
        current_game.won = won
        current_game.completed_at = datetime.utcnow()

        # Update student stats
        student.total_games += 1
        if won:
            student.total_wins += 1

        # Save solution for sharing
        solution = Solution(
            student_id=student.id,
            word=target_word,
            game_type='daily',
            solution_path=json.dumps([g['word'] for g in guesses]),
            guess_count=len(guesses),
            won=won
        )
        db.session.add(solution)

    db.session.commit()

    # Prepare response
    response_data = {
        'success': True,
        'result': result,
        'game_over': game_over,
        'won': won,
        'target_word': target_word if game_over else None,
        'guess_count': len(guesses)
    }

    if game_over:
        response_data['stats'] = {
            'total_games': student.total_games,
            'total_wins': student.total_wins,
            'win_rate': round(student.total_wins / student.total_games * 100, 1),
            'current_streak': calculate_current_streak(student.id)
        }

    return jsonify(response_data)

@app.route('/get_game_state')
def get_game_state():
    if 'student_id' not in session:
        return jsonify({'error': 'Not logged in'})

    student = Student.query.get(session['student_id'])
    if not student:
        return jsonify({'error': 'Student not found'})

    # Get current teacher word
    current_word = TeacherWord.query.order_by(TeacherWord.set_at.desc()).first()
    if not current_word:
        return jsonify({'guesses': [], 'game_over': False, 'won': False, 'has_word': False})

    # Get current game
    current_game = Game.query.filter_by(
        student_id=student.id,
        target_word=current_word.word
    ).first()

    if not current_game:
        return jsonify({'guesses': [], 'game_over': False, 'won': False, 'has_word': True})

    guesses = json.loads(current_game.guesses)

    return jsonify({
        'guesses': guesses,
        'game_over': current_game.completed,
        'won': current_game.won,
        'has_word': True
    })

@app.route('/daily/get_game_state')
def get_daily_game_state():
    if 'student_id' not in session:
        return jsonify({'error': 'Not logged in'})

    student = Student.query.get(session['student_id'])
    if not student:
        return jsonify({'error': 'Student not found'})

    today = date.today()

    # Get current daily game
    current_game = DailyGame.query.filter_by(
        student_id=student.id,
        date=today
    ).first()

    if not current_game:
        return jsonify({'guesses': [], 'game_over': False, 'won': False, 'has_word': True})

    guesses = json.loads(current_game.guesses)

    return jsonify({
        'guesses': guesses,
        'game_over': current_game.completed,
        'won': current_game.won,
        'has_word': True
    })

@app.route('/new_game', methods=['POST'])
def new_game():
    if 'student_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})

    student = Student.query.get(session['student_id'])
    current_word = TeacherWord.query.order_by(TeacherWord.set_at.desc()).first()

    if not current_word:
        return jsonify({'success': False, 'message': 'No word set'})

    # Create new game
    new_game = Game(
        student_id=student.id,
        target_word=current_word.word,
        guesses='[]',
        game_type='custom'
    )
    db.session.add(new_game)
    db.session.commit()

    return jsonify({'success': True})

@app.route('/daily/new_game', methods=['POST'])
def new_daily_game():
    if 'student_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})

    student = Student.query.get(session['student_id'])
    today = date.today()
    daily_word = get_daily_word()

    # Create new daily game
    new_game = DailyGame(
        student_id=student.id,
        target_word=daily_word,
        date=today,
        guesses='[]'
    )
    db.session.add(new_game)
    db.session.commit()

    return jsonify({'success': True})

@app.route('/student_search')
def student_search():
    return render_template('student_search.html')

@app.route('/search_students', methods=['POST'])
def search_students():
    search_term = request.json.get('search', '').strip().lower()
    thirty_days_ago = datetime.now() - timedelta(days=30)

    if not search_term:
        return jsonify({'students': []})

    # Search by name or username
    students = Student.query.filter(
        (Student.name.ilike(f'%{search_term}%')) |
        (Student.username.ilike(f'%{search_term}%'))
    ).all()

    student_data_list = []

    for student in students:
        # Get recent games (last 30 days)
        recent_custom = Game.query.filter(
            Game.student_id == student.id,
            Game.completed == True,
            Game.created_at >= thirty_days_ago
        ).count()

        recent_infinite = InfiniteGame.query.filter(
            InfiniteGame.student_id == student.id,
            InfiniteGame.completed == True,
            InfiniteGame.created_at >= thirty_days_ago
        ).count()

        recent_daily = DailyGame.query.filter(
            DailyGame.student_id == student.id,
            DailyGame.completed == True,
            DailyGame.date >= (datetime.now().date() - timedelta(days=30))
        ).count()

        # Get all completed games for totals
        total_custom = Game.query.filter_by(student_id=student.id, completed=True).count()
        total_infinite = InfiniteGame.query.filter_by(student_id=student.id, completed=True).count()
        total_daily = DailyGame.query.filter_by(student_id=student.id, completed=True).count()
        total_games = total_custom + total_infinite + total_daily

        # Get wins
        custom_wins = Game.query.filter_by(student_id=student.id, completed=True, won=True).count()
        infinite_wins = InfiniteGame.query.filter_by(student_id=student.id, completed=True, won=True).count()
        daily_wins = DailyGame.query.filter_by(student_id=student.id, completed=True, won=True).count()
        total_wins = custom_wins + infinite_wins + daily_wins

        # Calculate win rate
        win_rate = round((total_wins / total_games * 100), 1) if total_games > 0 else 0

        # Get streaks
        custom_streak = calculate_current_streak(student.id)
        infinite_streak = calculate_infinite_streak(student.id)
        daily_streak = calculate_daily_streak(student.id)

        # Calculate average guesses for won games
        custom_won_games = Game.query.filter_by(student_id=student.id, completed=True, won=True).all()
        infinite_won_games = InfiniteGame.query.filter_by(student_id=student.id, completed=True, won=True).all()
        daily_won_games = DailyGame.query.filter_by(student_id=student.id, completed=True, won=True).all()

        avg_guesses_custom = round(sum(g.guess_count for g in custom_won_games) / len(custom_won_games), 1) if custom_won_games else 0
        avg_guesses_infinite = round(sum(g.guess_count for g in infinite_won_games) / len(infinite_won_games), 1) if infinite_won_games else 0
        avg_guesses_daily = round(sum(g.guess_count for g in daily_won_games) / len(daily_won_games), 1) if daily_won_games else 0

        # Get last played date
        last_custom = Game.query.filter_by(student_id=student.id, completed=True).order_by(Game.completed_at.desc()).first()
        last_infinite = InfiniteGame.query.filter_by(student_id=student.id, completed=True).order_by(InfiniteGame.completed_at.desc()).first()
        last_daily = DailyGame.query.filter_by(student_id=student.id, completed=True).order_by(DailyGame.date.desc()).first()

        last_played = None
        dates = []
        if last_custom and last_custom.completed_at:
            dates.append(last_custom.completed_at)
        if last_infinite and last_infinite.completed_at:
            dates.append(last_infinite.completed_at)
        if last_daily:
            dates.append(datetime.combine(last_daily.date, datetime.min.time()))

        if dates:
            last_played = max(dates)

        student_data = {
            'id': student.id,
            'name': student.name,
            'username': student.username,
            'total_games': total_games,
            'total_wins': total_wins,
            'win_rate': win_rate,
            'custom_streak': custom_streak,
            'infinite_streak': infinite_streak,
            'daily_streak': daily_streak,
            'avg_guesses_custom': avg_guesses_custom,
            'avg_guesses_infinite': avg_guesses_infinite,
            'avg_guesses_daily': avg_guesses_daily,
            'recent_custom_games': recent_custom,
            'recent_infinite_games': recent_infinite,
            'recent_daily_games': recent_daily,
            'last_played': last_played.isoformat() if last_played else None
        }

        student_data_list.append(student_data)

    return jsonify({'students': student_data_list})

def calculate_infinite_streak(student_id):
    games = InfiniteGame.query.filter_by(
        student_id=student_id,
        completed=True
    ).order_by(InfiniteGame.completed_at.desc()).all()

    streak = 0
    for game in games:
        if game.won:
            streak += 1
        else:
            break

    return streak

def calculate_daily_streak(student_id):
    games = DailyGame.query.filter_by(
        student_id=student_id,
        completed=True
    ).order_by(DailyGame.date.desc()).all()

    streak = 0
    for game in games:
        if game.won:
            streak += 1
        else:
            break

    return streak

@app.route('/leaderboard')
def leaderboard():
    # Get top students by win rate (minimum 5 games)
    students_by_winrate = Student.query.filter(Student.total_games >= 5).order_by(
        (Student.total_wins * 100.0 / Student.total_games).desc()
    ).limit(10).all()

    # Get top students by total wins
    students_by_wins = Student.query.order_by(Student.total_wins.desc()).limit(10).all()

    # Get top students by total games
    students_by_games = Student.query.order_by(Student.total_games.desc()).limit(10).all()

    return render_template('leaderboard.html',
                         students_by_winrate=students_by_winrate,
                         students_by_wins=students_by_wins,
                         students_by_games=students_by_games)

@app.route('/student_stats/<int:student_id>/<game_type>')
def view_student_stats(student_id, game_type):
    student = Student.query.get_or_404(student_id)

    if game_type == 'infinite':
        games = InfiniteGame.query.filter_by(student_id=student_id, completed=True).order_by(InfiniteGame.completed_at.desc()).all()
        page_title = f"{student.name} - Infinite Wordle Stats"
        current_streak = calculate_infinite_streak(student_id)
        won_games = [g for g in games if g.won]
    elif game_type == 'daily':
        games = DailyGame.query.filter_by(student_id=student_id, completed=True).order_by(DailyGame.date.desc()).all()
        page_title = f"{student.name} - Daily Wordle Stats"
        current_streak = calculate_daily_streak(student_id)
        won_games = [g for g in games if g.won]
    else:
        games = Game.query.filter_by(student_id=student_id, completed=True).order_by(Game.completed_at.desc()).all()
        page_title = f"{student.name} - Custom Wordle Stats"
        current_streak = calculate_current_streak(student_id)
        won_games = [g for g in games if g.won]

    # Calculate average guesses for won games
    avg_guesses = round(sum(g.guess_count for g in won_games) / len(won_games), 1) if won_games else 0

    return render_template('student_stats.html',
                         student=student,
                         games=games,
                         game_type=game_type,
                         page_title=page_title,
                         current_streak=current_streak,
                         avg_guesses=avg_guesses)

@app.route('/teacher/student/<int:student_id>')
def view_student_details(student_id):
    if not session.get('teacher_authenticated'):
        return redirect(url_for('teacher_login'))

    student = Student.query.get_or_404(student_id)

    # Get comprehensive game statistics
    custom_games = Game.query.filter_by(student_id=student_id, completed=True).order_by(Game.completed_at.desc()).all()
    infinite_games = InfiniteGame.query.filter_by(student_id=student_id, completed=True).order_by(InfiniteGame.completed_at.desc()).all()
    daily_games = DailyGame.query.filter_by(student_id=student_id, completed=True).order_by(DailyGame.completed_at.desc()).all()

    # Calculate detailed statistics
    stats = {
        'custom_games': len(custom_games),
        'custom_wins': len([g for g in custom_games if g.won]),
        'custom_win_rate': round(len([g for g in custom_games if g.won]) / max(len(custom_games), 1) * 100, 1),
        'infinite_games': len(infinite_games),
        'infinite_wins': len([g for g in infinite_games if g.won]),
        'infinite_win_rate': round(len([g for g in infinite_games if g.won]) / max(len(infinite_games), 1) * 100, 1),
        'daily_games': len(daily_games),
        'daily_wins': len([g for g in daily_games if g.won]),
        'daily_win_rate': round(len([g for g in daily_games if g.won]) / max(len(daily_games), 1) * 100, 1),
        'fastest_solve': min([g.guess_count for g in custom_games + infinite_games + daily_games if g.won], default=0),
        'total_time_played': len(custom_games) + len(infinite_games) + len(daily_games),
        'perfect_games': len([g for g in custom_games + infinite_games + daily_games if g.won and g.guess_count == 1]),
        'current_custom_streak': calculate_current_streak(student_id),
        'current_infinite_streak': calculate_infinite_streak(student_id),
        'current_daily_streak': calculate_daily_streak(student_id)
    }

    # Get recent activity across all game types
    all_games = []
    for g in custom_games[:10]:
        all_games.append({'game': g, 'type': 'Custom'})
    for g in infinite_games[:10]:
        all_games.append({'game': g, 'type': 'Infinite'})
    for g in daily_games[:10]:
        all_games.append({'game': g, 'type': 'Daily'})

    # Sort by completion date
    all_games.sort(key=lambda x: x['game'].completed_at or datetime.min, reverse=True)
    recent_games = all_games[:15]

    return render_template('student_details.html',
                         student=student,
                         games=custom_games[:10],
                         stats=stats,
                         recent_games=recent_games)

@app.route('/student/infinite')
def infinite_wordle():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    student = Student.query.get(session['student_id'])
    if not student:
        return redirect(url_for('student_login'))

    current_game = InfiniteGame.query.filter_by(
        student_id=student.id,
        completed=False
    ).first()

    if not current_game:
        random_word = random.choice(WORD_LIST)
        current_game = InfiniteGame(
            student_id=student.id,
            target_word=random_word,
            guesses='[]'
        )
        db.session.add(current_game)
        db.session.commit()

    print(f"\u001b[31mTarget word for {student} is: {current_game.target_word}\033[0m")  # <-- Print target word

    return render_template('infinite_game.html', student=student, game=current_game)


@app.route('/infinite/make_guess', methods=['POST'])
def make_infinite_guess():

    if 'student_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})

    student = Student.query.get(session['student_id'])
    if not student:
        return jsonify({'success': False, 'message': 'Student not found'})

    guess = request.json.get('guess', '').upper().strip()

    # Get current infinite game
    current_game = InfiniteGame.query.filter_by(
        student_id=student.id,
        completed=False
    ).first()

    if not current_game:
        return jsonify({'success': False, 'message': 'No active game found'})

    if current_game.completed:
        return jsonify({'success': False, 'message': 'Game is already over!'})

    if len(guess) != 5 or not guess.isalpha():
        return jsonify({'success': False, 'message': 'Guess must be exactly 5 letters!'})

    # Parse current guesses
    guesses = json.loads(current_game.guesses)

    if len(guesses) >= 6:
        return jsonify({'success': False, 'message': 'No more guesses allowed!'})

    target_word = current_game.target_word.upper()

    # ✅ Proper Wordle logic (handles duplicates correctly)
    result = ['absent'] * 5
    target_letters = list(target_word)

    # First pass: correct letters
    for i in range(5):
        if guess[i] == target_letters[i]:
            result[i] = 'correct'
            target_letters[i] = None  # mark as used

    # Second pass: present letters
    for i in range(5):
        if result[i] == 'correct':
            continue
        if guess[i] in target_letters:
            result[i] = 'present'
            target_letters[target_letters.index(guess[i])] = None  # remove used letter

    # Add guess to game
    guesses.append({
        'word': guess,
        'result': result
    })

    current_game.guesses = json.dumps(guesses)
    current_game.guess_count = len(guesses)

    # Check if won or game over
    won = guess == target_word
    game_over = won or len(guesses) >= 6

    if game_over:
        current_game.completed = True
        current_game.won = won
        current_game.completed_at = datetime.utcnow()

        # Update student stats
        student.total_games += 1
        if won:
            student.total_wins += 1

        solution = Solution(
            student_id=student.id,
            word=target_word,
            game_type='infinite',
            solution_path=json.dumps([g['word'] for g in guesses]),
            guess_count=len(guesses),
            won=won
        )
        db.session.add(solution)

    db.session.commit()

    response_data = {
        'success': True,
        'result': result,
        'game_over': game_over,
        'won': won,
        'target_word': target_word if game_over else None,
        'guess_count': len(guesses)
    }

    if game_over:
        infinite_streak = calculate_infinite_streak(student.id)
        response_data['stats'] = {
            'total_games': student.total_games,
            'total_wins': student.total_wins,
            'win_rate': round(student.total_wins / student.total_games * 100, 1),
            'current_streak': infinite_streak
        }

    return jsonify(response_data)

@app.route('/infinite/get_game_state')
def get_infinite_game_state():
    if 'student_id' not in session:
        return jsonify({'error': 'Not logged in'})

    student = Student.query.get(session['student_id'])
    if not student:
        return jsonify({'error': 'Student not found'})

        # Get current infinite game
    current_game = InfiniteGame.query.filter_by(
        student_id=student.id,
        completed=False
    ).first()

    if not current_game:
        return jsonify({'guesses': [], 'game_over': False, 'won': False, 'has_word': True})

    guesses = json.loads(current_game.guesses)

    # Print the target word to the server console
    print(f"Current word for student {student.id}: {current_game.target_word}")

    return jsonify({
            'guesses': guesses,
            'game_over': current_game.completed,
            'won': current_game.won,
            'has_word': True
        })

@app.route('/infinite/new_game', methods=['POST'])
def new_infinite_game():
    if 'student_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})

    student = Student.query.get(session['student_id'])

    # Create new infinite game with random word
    random_word = random.choice(WORD_LIST)
    new_game = InfiniteGame(
        student_id=student.id,
        target_word=random_word,
        guesses='[]'
    )
    db.session.add(new_game)
    db.session.commit()

    return jsonify({'success': True})

@app.route('/solutions/<word>/<game_type>')
def view_solutions(word, game_type):
    word = word.upper()

    solutions = (
        Solution.query
        .filter_by(word=word, game_type=game_type)
        .options(joinedload(Solution.student))
        .order_by(Solution.won.desc(), Solution.guess_count.asc())
        .all()
    )

    # ✅ Parse JSON safely here
    for s in solutions:
        try:
            s.solution_list = json.loads(s.solution_path)
        except:
            s.solution_list = []

    winning_solutions = [s for s in solutions if s.won]
    recommended = winning_solutions[0] if winning_solutions else None

    return render_template(
        'solutions.html',
        word=word,
        game_type=game_type,
        solutions=solutions,
        recommended=recommended,
        total_solutions=len(solutions),
        total_wins=len(winning_solutions)
    )

def calculate_current_streak(student_id):
    games = Game.query.filter_by(student_id=student_id, completed=True).order_by(Game.completed_at.desc()).all()
    streak = 0
    for game in games:
        if game.won:
            streak += 1
        else:
            break
    return streak

def calculate_daily_streak(student_id):
    games = DailyGame.query.filter_by(student_id=student_id, completed=True).order_by(DailyGame.date.desc()).all()
    streak = 0
    for game in games:
        if game.won:
            streak += 1
        else:
            break
    return streak

@app.route('/teacher/get_student_password/<int:student_id>')
def get_student_password(student_id):
    if not session.get('teacher_authenticated'):
        return jsonify({'success': False, 'message': 'Not authorized'})

    student = Student.query.get_or_404(student_id)

    # Return the actual password if available, otherwise show default
    actual_password = student.plain_password if student.plain_password else 'password123'

    return jsonify({
        'success': True,
        'password': actual_password,
        'username': student.username
    })

@app.route('/teacher/password_management')
def password_management():
    if not session.get('teacher_authenticated'):
        return redirect(url_for('teacher_login'))

    # Get all students
    students = Student.query.all()

    return render_template('password_management.html', students=students)

@app.route('/teacher/update_student_password', methods=['POST'])
def update_student_password():
    if not session.get('teacher_authenticated'):
        return jsonify({'success': False, 'message': 'Not authorized'})

    data = request.json
    student_id = data.get('student_id')
    new_password = data.get('new_password')

    if not student_id or not new_password:
        return jsonify({'success': False, 'message': 'Missing data'})

    if len(new_password) < 4:
        return jsonify({'success': False, 'message': 'Password must be at least 4 characters'})

    student = Student.query.get(student_id)
    if not student:
        return jsonify({'success': False, 'message': 'Student not found'})

    # Update password
    student.password_hash = Student.hash_password(new_password)
    student.plain_password = new_password  # Store plain password for teacher access
    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'Password updated for {student.name}'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)