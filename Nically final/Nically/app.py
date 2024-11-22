import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, is_valid_email, is_secure_password
from datetime import timedelta, datetime
import re

# Configure application
app = Flask(__name__)
db = SQL("sqlite:///users.db")

# Configure session
app.config["SESSION_TYPE"] = "filesystem"
app.config["UPLOAD_FOLDER"] = "/static"
app.permanent_session_lifetime = timedelta(minutes=60)
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Toggle dark mode
@app.route("/toggle-dark-mode", methods=["POST"])
def toggle_dark_mode():
    if session.get("dark-mode") == "enabled":
        session["dark-mode"] = "disabled"
    else:
        session["dark-mode"] = "enabled"
    return ("", 204)

# Main route
@app.route("/")
def index():
    if "user_id" in session:
        user_id = session["user_id"]

        username = db.execute("SELECT username FROM users WHERE id = ?", user_id)
        username = username[0]["username"]

        # Validar logros existentes
        completed_trivias = db.execute(
            "SELECT COUNT(DISTINCT trivia_id) AS total_completed FROM user_trivias WHERE user_id = :user_id",
            user_id=user_id
        )[0]["total_completed"]

        # Verificar y asignar logros según el progreso
        achievements_to_check = [
            {"id": 1, "condition": completed_trivias >= 1},  # Principiante: Completó 1 trivia
            {"id": 2, "condition": completed_trivias >= 3},  # Uwu: Completó 3 trivias
            {"id": 3, "condition": completed_trivias >= 5},  # Pinolero: Completó todas las trivias
        ]

        for achievement in achievements_to_check:
            # Verificar si ya tiene el logro asignado
            exists = db.execute(
                """
                SELECT 1 FROM user_achievements
                WHERE user_id = :user_id AND achievement_id = :achievement_id
                """,
                user_id=user_id,
                achievement_id=achievement["id"]
            )
            # Si no lo tiene y cumple la condición, agregar el logro
            if not exists and achievement["condition"]:
                db.execute(
                    """
                    INSERT INTO user_achievements (user_id, achievement_id)
                    VALUES (:user_id, :achievement_id)
                    """,
                    user_id=user_id,
                    achievement_id=achievement["id"]
                )

        # Obtener categorías y trivias para mostrar en el index
        categories = db.execute("SELECT * FROM categories")
        trivias = db.execute(
            """
            SELECT t.trivia_id, t.title, t.image, c.name as category_name
            FROM trivias t
            JOIN categories c ON t.category_id = c.category_id
            """
        )
        return render_template("index.html", categories=categories, trivias=trivias, user_id = user_id, username = username)

    # Redirigir al registro si no hay sesión activa
    return redirect("/register")


# User registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        gmail = request.form.get("gmail")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not gmail or not is_valid_email(gmail):
            return render_template("register.html", error_message="Por favor, introduce un correo electrónico válido.")

        existing_user = db.execute("SELECT * FROM users WHERE gmail = ?", gmail)
        if existing_user:
            return render_template("register.html", error_message="El correo ya está registrado.")

        if not is_secure_password(password):
            return render_template("register.html", error_message="La contraseña no es segura, añade al menos un número, mayúscula y símbolo especial.")
        if password != confirmation:
            return render_template("register.html", error_message="Las contraseñas no coinciden.")

        password_hash = generate_password_hash(password)
        db.execute("INSERT INTO users (gmail, password) VALUES (?, ?)", gmail, password_hash)
        return redirect("/login")
    else:
        return render_template("register.html")

# User login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        gmail = request.form.get("gmail")
        password = request.form.get("password")

        if not gmail or not password:
            return render_template("login.html", error_message="Debes completar ambos campos.")

        user = db.execute("SELECT * FROM users WHERE gmail = ?", gmail)
        if not user or not check_password_hash(user[0]["password"], password):
            return render_template("login.html", error_message="Correo o contraseña incorrectos.")

        session["user_id"] = user[0]["id"]
        session.permanent = True
        return redirect("/profile")
    return render_template("login.html")

# User profile
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    current_date = datetime.now().strftime('%Y-%m-%d')
    if request.method == "POST":
        username = request.form.get("username")
        gender = request.form.get("gender")
        birthday = request.form.get("birthday")

        if not username or not gender or not birthday or birthday > current_date:
            return render_template("profile.html", error_message="Datos inválidos.", current_date=current_date)

        db.execute("UPDATE users SET username = ?, gender = ?, birthday = ? WHERE id = ?", username, gender, birthday, session["user_id"])
        return redirect("/")
    return render_template("profile.html", current_date=current_date)


@app.route("/user_profile", methods=["GET"])
@login_required
def user_profile():
    user_id = session["user_id"]

    # Consultar los datos del usuario
    user_data = db.execute("SELECT * FROM users WHERE id = ?", user_id)
    username = user_data[0]["username"]
    gender = user_data[0]["gender"]
    birthday = user_data[0]["birthday"]

    # Consultar los logros del usuario
    achievements_data = db.execute("SELECT * FROM user_achievements WHERE user_id = ?", user_id)
    achievements = [achievement["title"] for achievement in achievements_data]

    return render_template("user_profile.html", username=username, genre=gender, birthday=birthday, achievements=achievements)






# Trivia gameplay
import random

@app.route("/trivia/<int:trivia_id>")
@login_required
def trivia(trivia_id):
    user_id = session["user_id"]

    # Obtener la trivia y verificar si existe
    trivia = db.execute("SELECT * FROM trivias WHERE trivia_id = ?", trivia_id)
    if not trivia:
        return redirect("/")

    trivia = trivia[0]

    unanswered_questions = db.execute(
        """
        SELECT q.*
        FROM questions q
        WHERE q.trivia_id = ?
        AND NOT EXISTS (
            SELECT 1
            FROM user_responses ur
            JOIN responses r ON ur.response_id = r.response_id
            WHERE ur.user_id = ? AND ur.correct = 1 AND r.question_id = q.question_id
        )
        ORDER BY q.question_id
        """,
        trivia_id, user_id,
    )

    if not unanswered_questions:
        flash("Ya completaste esta trivia.", "success")
        return redirect("/")

    # Barajar las preguntas
    random.shuffle(unanswered_questions)
    question = unanswered_questions[0]

    # Obtener las respuestas de la pregunta actual
    responses = db.execute(
        "SELECT * FROM responses WHERE question_id = ?", question["question_id"]
    )

    # Barajar las respuestas
    random.shuffle(responses)

    # Contar preguntas y progreso
    total_questions = db.execute(
        "SELECT COUNT(*) as total FROM questions WHERE trivia_id = ?", trivia_id
    )[0]["total"]

    answered_count = db.execute(
        """
        SELECT COUNT(*) as count
        FROM user_responses ur
        JOIN responses r ON ur.response_id = r.response_id
        JOIN questions q ON r.question_id = q.question_id
        WHERE ur.user_id = ? AND q.trivia_id = ?
        """,
        user_id, trivia_id,
    )[0]["count"]

    return render_template(
        "trivia.html",
        trivia=trivia,
        question=question,
        responses=responses,
        question_num=answered_count + 1,
        total_questions=total_questions,
    )


@app.route("/register_response/<int:trivia_id>/<int:response_id>", methods=["POST"])
@login_required
def register_response(trivia_id, response_id):
    user_id = session["user_id"]

    # Verificar si la trivia ya fue completada
    correct_answers = db.execute(
        """
        SELECT COUNT(DISTINCT q.question_id) as correct_count
        FROM questions q
        JOIN responses r ON q.question_id = r.question_id
        JOIN user_responses ur ON ur.response_id = r.response_id
        WHERE ur.user_id = ? AND q.trivia_id = ? AND ur.correct = 1
        """,
        user_id, trivia_id
    )[0]["correct_count"]

    total_questions = db.execute(
        "SELECT COUNT(*) as total FROM questions WHERE trivia_id = ?", trivia_id
    )[0]["total"]

    if correct_answers >= total_questions:
        flash("¡Ya completaste esta trivia anteriormente!", "info")
        return redirect("/")

    # Verificar información de la respuesta seleccionada
    response = db.execute(
        """
        SELECT r.correct, q.question_id
        FROM responses r
        JOIN questions q ON r.question_id = q.question_id
        WHERE r.response_id = ? AND q.trivia_id = ?
        """,
        response_id, trivia_id,
    )

    if not response:
        flash("Pregunta no encontrada. Inténtalo nuevamente.", "error")
        return redirect("/")

    correct = response[0]["correct"]

    # Registrar respuesta solo si aún no existe un registro para esta respuesta
    db.execute(
        """
        INSERT INTO user_responses (user_id, trivia_id, response_id, correct)
        VALUES (?, ?, ?, ?)
        ON CONFLICT DO NOTHING;
        """,
        user_id, trivia_id, response_id, correct,
    )

    # Mostrar mensaje según si la respuesta es correcta o incorrecta
    if correct:
        flash("¡Respuesta correcta! Sigue con la próxima pregunta.", "success")
    else:
        flash("Respuesta incorrecta. Sigue intentando.", "error")

    # Verificar progreso del usuario
    correct_count = db.execute(
        """
        SELECT COUNT(DISTINCT q.question_id) as count
        FROM questions q
        JOIN responses r ON q.question_id = r.question_id
        JOIN user_responses ur ON ur.response_id = r.response_id
        WHERE ur.user_id = ? AND q.trivia_id = ? AND ur.correct = 1
        """,
        user_id, trivia_id,
    )[0]["count"]

    total_questions = db.execute(
        "SELECT COUNT(*) as total FROM questions WHERE trivia_id = ?", trivia_id
    )[0]["total"]

    # Si todas las preguntas fueron respondidas correctamente, registrar como completada
    if correct_count >= total_questions:
        db.execute(
            """
            INSERT OR IGNORE INTO user_trivias (user_id, trivia_id, date_played)
            VALUES (?, ?, DATE('now'))
            """,
            user_id, trivia_id,
        )
        flash("¡Felicidades, completaste la trivia con todas las respuestas correctas!", "success")
        return redirect("/")

    # Obtener la siguiente pregunta no respondida o respondida incorrectamente
    next_question = db.execute(
        """
        SELECT q.*
        FROM questions q
        WHERE q.trivia_id = ?
        AND NOT EXISTS (
            SELECT 1
            FROM user_responses ur
            JOIN responses r ON ur.response_id = r.response_id
            WHERE ur.user_id = ? AND r.question_id = q.question_id AND ur.correct = 1
        )
        ORDER BY q.question_id
        LIMIT 1
        """,
        trivia_id, user_id
    )

    if not next_question:
        flash("No hay más preguntas disponibles.", "error")
        return redirect("/")

    # Obtener las respuestas para la siguiente pregunta
    responses = db.execute(
        "SELECT * FROM responses WHERE question_id = ?", next_question[0]["question_id"]
    )

    return render_template(
        "trivia.html",
        trivia=db.execute("SELECT * FROM trivias WHERE trivia_id = ?", trivia_id)[0],
        question=next_question[0],
        responses=responses,
        question_num=correct_count + 1,
        total_questions=total_questions,
    )


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.pop("user_id", None)

    # Redirect user to login form
    return redirect("/login")


# Additional routes (Wiki, Trophy, Settings)
@app.route("/enciclopedia")
def wiki():
    return render_template("wiki.html")


@app.route("/achievements")
def trophy():
    # Obtener los logros desbloqueados por el usuario
    user_achievements = db.execute("""
        SELECT achievements.title, achievements.description
        FROM achievements
        JOIN user_achievements ON achievements.achievement_id = user_achievements.achievement_id
        WHERE user_achievements.user_id = :user_id
    """, user_id=session["user_id"])  # Filtramos los logros por el usuario actual

    return render_template("achievements.html", achievements=user_achievements)



@app.route("/settings")
def settings():
    return render_template("settings.html")
