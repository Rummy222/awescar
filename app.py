import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User, Category, Nominee, Prediction, Setting

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "oscars2025")

# Heroku provides DATABASE_URL with postgres:// scheme; SQLAlchemy requires postgresql://
_db_url = os.environ.get("DATABASE_URL", "sqlite:///awescar.db")
if _db_url.startswith("postgres://"):
    _db_url = _db_url.replace("postgres://", "postgresql://", 1)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-me-in-production")
app.config["SQLALCHEMY_DATABASE_URI"] = _db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.before_request
def redirect_to_https_and_apex():
    # Redirect HTTP → HTTPS
    if request.headers.get("X-Forwarded-Proto") == "http":
        return redirect(request.url.replace("http://", "https://", 1), code=301)
    # Redirect www → apex domain
    if request.host.startswith("www."):
        return redirect("https://awescar.org" + request.full_path.rstrip("?"), code=301)


# ── helpers ──────────────────────────────────────────────────────────────────

def current_user():
    uid = session.get("user_id")
    if uid:
        return db.session.get(User, uid)
    return None


def predictions_locked():
    s = db.session.get(Setting, "predictions_locked")
    return s is not None and s.value == "true"


def is_admin():
    return session.get("is_admin", False)


@app.context_processor
def inject_globals():
    return {
        "current_user": current_user(),
        "is_admin": is_admin(),
        "predictions_locked": predictions_locked(),
    }


# ── public routes ─────────────────────────────────────────────────────────────

@app.route("/")
def index():
    categories = Category.query.order_by(Category.display_order).all()
    user = current_user()
    user_preds = {}
    if user:
        for p in user.predictions:
            user_preds[p.category_id] = p.nominee_id
    total = len(categories)
    revealed = sum(1 for c in categories if c.winner)
    return render_template("index.html", categories=categories,
                           user_preds=user_preds, total=total, revealed=revealed)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        if not username or len(username) < 2:
            flash("Username must be at least 2 characters.", "danger")
            return redirect(url_for("login"))
        if len(username) > 30:
            flash("Username must be 30 characters or fewer.", "danger")
            return redirect(url_for("login"))
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
            flash(f"Welcome to the Oscars Pool, {username}!", "success")
        else:
            flash(f"Welcome back, {username}!", "success")
        session["user_id"] = user.id
        if user.is_admin:
            session["is_admin"] = True
        return redirect(url_for("predictions"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("index"))


@app.route("/predictions", methods=["GET", "POST"])
def predictions():
    user = current_user()
    if not user:
        flash("Please log in to make predictions.", "warning")
        return redirect(url_for("login"))

    locked = predictions_locked()

    if request.method == "POST":
        if locked:
            flash("Predictions are locked.", "danger")
            return redirect(url_for("predictions"))

        for key, value in request.form.items():
            if not key.startswith("cat_"):
                continue
            try:
                category_id = int(key[4:])
                nominee_id = int(value)
            except ValueError:
                continue
            nominee = Nominee.query.filter_by(id=nominee_id,
                                              category_id=category_id).first()
            if not nominee:
                continue
            pred = Prediction.query.filter_by(user_id=user.id,
                                              category_id=category_id).first()
            if pred:
                pred.nominee_id = nominee_id
            else:
                db.session.add(Prediction(user_id=user.id,
                                          category_id=category_id,
                                          nominee_id=nominee_id))
        db.session.commit()
        flash("Predictions saved!", "success")
        return redirect(url_for("predictions"))

    categories = Category.query.order_by(Category.display_order).all()
    user_preds = {p.category_id: p.nominee_id for p in user.predictions}
    picked = len(user_preds)
    total = len(categories)
    return render_template("predictions.html", categories=categories,
                           user_preds=user_preds, picked=picked, total=total,
                           locked=locked)


@app.route("/leaderboard")
def leaderboard():
    categories = Category.query.order_by(Category.display_order).all()
    total = len(categories)
    revealed = sum(1 for c in categories if c.winner)

    users = User.query.filter_by(is_admin=False).all()
    board = []
    for u in users:
        preds = {p.category_id: p.nominee_id for p in u.predictions}
        correct = sum(
            1 for c in categories
            if c.winner and preds.get(c.id) == c.winner.id
        )
        board.append({
            "user": u,
            "correct": correct,
            "picked": len(preds),
            "accuracy": round(correct / revealed * 100) if revealed else 0,
        })
    board.sort(key=lambda x: (-x["correct"], x["user"].username))
    for i, entry in enumerate(board):
        entry["rank"] = i + 1

    user = current_user()
    return render_template("leaderboard.html", board=board, total=total,
                           revealed=revealed, current_user_id=user.id if user else None)


# ── admin routes ──────────────────────────────────────────────────────────────

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        action = request.form.get("action")

        if action == "login":
            if request.form.get("password") == ADMIN_PASSWORD:
                session["is_admin"] = True
                flash("Admin access granted.", "success")
            else:
                flash("Invalid password.", "danger")
            return redirect(url_for("admin"))

        if not is_admin():
            flash("Admin access required.", "danger")
            return redirect(url_for("admin"))

        if action == "set_winner":
            nominee_id = int(request.form.get("nominee_id"))
            next_cat = request.form.get("next_cat", "")
            nominee = db.session.get(Nominee, nominee_id)
            if nominee:
                Nominee.query.filter_by(category_id=nominee.category_id).update(
                    {"is_winner": False})
                nominee.is_winner = True
                db.session.commit()
            dest = url_for("admin") + (f"?cat={next_cat}" if next_cat else "")
            return redirect(dest)

        elif action == "clear_winner":
            category_id = int(request.form.get("category_id"))
            next_cat = request.form.get("next_cat", "")
            Nominee.query.filter_by(category_id=category_id).update({"is_winner": False})
            db.session.commit()
            dest = url_for("admin") + (f"?cat={next_cat}" if next_cat else "")
            return redirect(dest)

        elif action == "toggle_lock":
            s = db.session.get(Setting, "predictions_locked")
            if not s:
                s = Setting(key="predictions_locked", value="false")
                db.session.add(s)
            s.value = "false" if s.value == "true" else "true"
            db.session.commit()
            flash(f"Predictions {'locked' if s.value == 'true' else 'unlocked'}.", "info")

        elif action == "admin_logout":
            session.pop("is_admin", None)
            flash("Admin session ended.", "info")
            return redirect(url_for("index"))

        return redirect(url_for("admin"))

    if not is_admin():
        return render_template("admin_login.html")

    categories = Category.query.order_by(Category.display_order).all()
    locked = predictions_locked()

    # Determine active category for live mode
    cat_param = request.args.get("cat")
    active_cat = None
    if cat_param:
        active_cat = next((c for c in categories if c.id == int(cat_param)), None)
    if not active_cat:
        # Default to first unpicked, or last category if all done
        active_cat = next((c for c in categories if not c.winner), categories[-1])

    # Next unpicked after active_cat (for auto-advance)
    unpicked = [c for c in categories if not c.winner and c.id != active_cat.id]
    next_unpicked = unpicked[0] if unpicked else None

    revealed = sum(1 for c in categories if c.winner)
    return render_template("admin.html", categories=categories, locked=locked,
                           active_cat=active_cat, next_unpicked=next_unpicked,
                           revealed=revealed)


if __name__ == "__main__":
    app.run(debug=True, port=5002)
