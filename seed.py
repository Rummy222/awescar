"""Seed the database with 97th Academy Awards nominees (2025 ceremony)."""
from app import app
from models import db, Category, Nominee, Setting

CATEGORIES = [
    {
        "name": "Best Picture",
        "order": 1,
        "nominees": [
            ("Anora", ""),
            ("The Brutalist", ""),
            ("A Complete Unknown", ""),
            ("Conclave", ""),
            ("Dune: Part Two", ""),
            ("Emilia Pérez", ""),
            ("I'm Still Here", ""),
            ("Nickel Boys", ""),
            ("The Substance", ""),
            ("Wicked", ""),
        ],
    },
    {
        "name": "Best Director",
        "order": 2,
        "nominees": [
            ("Sean Baker", "Anora"),
            ("Brady Corbet", "The Brutalist"),
            ("James Mangold", "A Complete Unknown"),
            ("Jacques Audiard", "Emilia Pérez"),
            ("Coralie Fargeat", "The Substance"),
        ],
    },
    {
        "name": "Best Actress",
        "order": 3,
        "nominees": [
            ("Cynthia Erivo", "Wicked"),
            ("Karla Sofía Gascón", "Emilia Pérez"),
            ("Mikey Madison", "Anora"),
            ("Demi Moore", "The Substance"),
            ("Fernanda Torres", "I'm Still Here"),
        ],
    },
    {
        "name": "Best Actor",
        "order": 4,
        "nominees": [
            ("Adrien Brody", "The Brutalist"),
            ("Timothée Chalamet", "A Complete Unknown"),
            ("Colman Domingo", "Sing Sing"),
            ("Ralph Fiennes", "Conclave"),
            ("Sebastian Stan", "A Different Man"),
        ],
    },
    {
        "name": "Best Supporting Actress",
        "order": 5,
        "nominees": [
            ("Monica Barbaro", "A Complete Unknown"),
            ("Ariana Grande", "Wicked"),
            ("Felicity Jones", "The Brutalist"),
            ("Isabella Rossellini", "Conclave"),
            ("Zoe Saldana", "Emilia Pérez"),
        ],
    },
    {
        "name": "Best Supporting Actor",
        "order": 6,
        "nominees": [
            ("Yura Borisov", "Anora"),
            ("Kieran Culkin", "A Real Pain"),
            ("Edward Norton", "A Complete Unknown"),
            ("Jeremy Strong", "The Apprentice"),
            ("Zach Galifianakis", "A Real Pain"),
        ],
    },
    {
        "name": "Best Original Screenplay",
        "order": 7,
        "nominees": [
            ("Anora", "Sean Baker"),
            ("The Brutalist", "Brady Corbet & Mona Fastvold"),
            ("A Real Pain", "Jesse Eisenberg"),
            ("September 5", "Moritz Binder, Tim Fehlbaum & Alex David"),
            ("The Substance", "Coralie Fargeat"),
        ],
    },
    {
        "name": "Best Adapted Screenplay",
        "order": 8,
        "nominees": [
            ("A Complete Unknown", "James Mangold & Jay Cocks"),
            ("Conclave", "Peter Straughan"),
            ("Emilia Pérez", "Jacques Audiard"),
            ("Nickel Boys", "RaMell Ross & Joslyn Barnes"),
            ("Sing Sing", "Clint Bentley & Greg Kwedar"),
        ],
    },
    {
        "name": "Best Animated Feature Film",
        "order": 9,
        "nominees": [
            ("Flow", ""),
            ("Inside Out 2", ""),
            ("Memoir of a Snail", ""),
            ("Wallace & Gromit: Vengeance Most Fowl", ""),
            ("The Wild Robot", ""),
        ],
    },
    {
        "name": "Best International Feature Film",
        "order": 10,
        "nominees": [
            ("The Girl with the Needle", "Denmark / Poland"),
            ("I'm Still Here", "Brazil"),
            ("The Seed of the Sacred Fig", "Germany"),
            ("Vermiglio", "Italy"),
            ("Flow", "Latvia"),
        ],
    },
    {
        "name": "Best Documentary Feature Film",
        "order": 11,
        "nominees": [
            ("Black Box Diaries", ""),
            ("No Other Land", ""),
            ("Porcelain War", ""),
            ("Soundtrack to a Coup d'Etat", ""),
            ("Sugarcane", ""),
        ],
    },
    {
        "name": "Best Original Score",
        "order": 12,
        "nominees": [
            ("The Brutalist", "Daniel Blumberg"),
            ("Conclave", "Volker Bertelmann"),
            ("Emilia Pérez", "Clément Ducol & Camille"),
            ("Wicked", "John Powell & Stephen Schwartz"),
            ("The Wild Robot", "Kris Bowers"),
        ],
    },
    {
        "name": "Best Original Song",
        "order": 13,
        "nominees": [
            ("El Mal", "Emilia Pérez"),
            ("The Journey", "The Six Triple Eight"),
            ("Like A Bird", "Sing Sing"),
            ("Mi Camino", "Emilia Pérez"),
            ("Never Too Late", "Elton John: Never Too Late"),
        ],
    },
    {
        "name": "Best Cinematography",
        "order": 14,
        "nominees": [
            ("The Brutalist", "Lol Crawley"),
            ("Dune: Part Two", "Greig Fraser"),
            ("Emilia Pérez", "Paul Guilhaume"),
            ("Maria", "Ed Lachman"),
            ("Nosferatu", "Jarin Blaschke"),
        ],
    },
    {
        "name": "Best Film Editing",
        "order": 15,
        "nominees": [
            ("Anora", "Nicolas Gaster"),
            ("The Brutalist", "David Jancso"),
            ("Conclave", "Nick Emerson"),
            ("Emilia Pérez", "Juliette Welfling"),
            ("Wicked", "Myron Kerstein"),
        ],
    },
]


def seed():
    with app.app_context():
        db.create_all()
        if Category.query.count() > 0:
            print("Database already seeded. Use --force to re-seed.")
            return

        for cat_data in CATEGORIES:
            cat = Category(name=cat_data["name"], display_order=cat_data["order"])
            db.session.add(cat)
            db.session.flush()
            for name, detail in cat_data["nominees"]:
                db.session.add(Nominee(category_id=cat.id, name=name, detail=detail))

        if not db.session.get(Setting, "predictions_locked"):
            db.session.add(Setting(key="predictions_locked", value="false"))

        db.session.commit()
        print(f"Seeded {len(CATEGORIES)} categories with nominees.")


if __name__ == "__main__":
    import sys
    if "--force" in sys.argv:
        with app.app_context():
            Nominee.query.delete()
            Category.query.delete()
            db.session.commit()
    seed()
