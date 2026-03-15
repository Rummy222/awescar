"""Seed the database with 98th Academy Awards nominees (2026 ceremony)."""
from app import app
from models import db, Category, Nominee, Setting

CATEGORIES = [
    {
        "name": "Best Picture",
        "order": 1,
        "nominees": [
            ("Bugonia", ""),
            ("F1", ""),
            ("Frankenstein", ""),
            ("Hamnet", ""),
            ("Marty Supreme", ""),
            ("One Battle after Another", ""),
            ("The Secret Agent", ""),
            ("Sentimental Value", ""),
            ("Sinners", ""),
            ("Train Dreams", ""),
        ],
    },
    {
        "name": "Best Director",
        "order": 2,
        "nominees": [
            ("Chloé Zhao", "Hamnet"),
            ("Josh Safdie", "Marty Supreme"),
            ("Paul Thomas Anderson", "One Battle after Another"),
            ("Joachim Trier", "Sentimental Value"),
            ("Ryan Coogler", "Sinners"),
        ],
    },
    {
        "name": "Best Actress",
        "order": 3,
        "nominees": [
            ("Jessie Buckley", "Hamnet"),
            ("Rose Byrne", "If I Had Legs I'd Kick You"),
            ("Kate Hudson", "Song Sung Blue"),
            ("Renate Reinsve", "Sentimental Value"),
            ("Emma Stone", "Bugonia"),
        ],
    },
    {
        "name": "Best Actor",
        "order": 4,
        "nominees": [
            ("Timothée Chalamet", "Marty Supreme"),
            ("Leonardo DiCaprio", "One Battle after Another"),
            ("Ethan Hawke", "Blue Moon"),
            ("Michael B. Jordan", "Sinners"),
            ("Wagner Moura", "The Secret Agent"),
        ],
    },
    {
        "name": "Best Supporting Actress",
        "order": 5,
        "nominees": [
            ("Elle Fanning", "Sentimental Value"),
            ("Inga Ibsdotter Lilleaas", "Sentimental Value"),
            ("Amy Madigan", "Weapons"),
            ("Wunmi Mosaku", "Sinners"),
            ("Teyana Taylor", "One Battle after Another"),
        ],
    },
    {
        "name": "Best Supporting Actor",
        "order": 6,
        "nominees": [
            ("Benicio Del Toro", "One Battle after Another"),
            ("Jacob Elordi", "Frankenstein"),
            ("Delroy Lindo", "Sinners"),
            ("Sean Penn", "One Battle after Another"),
            ("Stellan Skarsgård", "Sentimental Value"),
        ],
    },
    {
        "name": "Best Original Screenplay",
        "order": 7,
        "nominees": [
            ("Blue Moon", "Robert Kaplow"),
            ("It Was Just an Accident", "Jafar Panahi"),
            ("Marty Supreme", "Ronald Bronstein & Josh Safdie"),
            ("Sentimental Value", "Eskil Vogt & Joachim Trier"),
            ("Sinners", "Ryan Coogler"),
        ],
    },
    {
        "name": "Best Adapted Screenplay",
        "order": 8,
        "nominees": [
            ("Bugonia", "Will Tracy"),
            ("Frankenstein", "Guillermo del Toro"),
            ("Hamnet", "Chloé Zhao & Maggie O'Farrell"),
            ("One Battle after Another", "Paul Thomas Anderson"),
            ("Train Dreams", "Clint Bentley & Greg Kwedar"),
        ],
    },
    {
        "name": "Best Animated Feature Film",
        "order": 9,
        "nominees": [
            ("Arco", "Ugo Bienvenu, Félix de Givry & Natalie Portman"),
            ("Elio", "Madeline Sharafian & Domee Shi"),
            ("KPop Demon Hunters", "Maggie Kang & Chris Appelhans"),
            ("Little Amélie or the Character of Rain", "Maïlys Vallade"),
            ("Zootopia 2", "Jared Bush & Byron Howard"),
        ],
    },
    {
        "name": "Best International Feature Film",
        "order": 10,
        "nominees": [
            ("The Secret Agent", "Brazil"),
            ("It Was Just an Accident", "France"),
            ("Sentimental Value", "Norway"),
            ("Sirāt", "Spain"),
            ("The Voice of Hind Rajab", "Tunisia"),
        ],
    },
    {
        "name": "Best Documentary Feature Film",
        "order": 11,
        "nominees": [
            ("The Alabama Solution", ""),
            ("Come See Me in the Good Light", ""),
            ("Cutting through Rocks", ""),
            ("Mr. Nobody against Putin", ""),
            ("The Perfect Neighbor", ""),
        ],
    },
    {
        "name": "Best Original Score",
        "order": 12,
        "nominees": [
            ("Bugonia", "Jerskin Fendrix"),
            ("Frankenstein", "Alexandre Desplat"),
            ("Hamnet", "Max Richter"),
            ("One Battle after Another", "Jonny Greenwood"),
            ("Sinners", "Ludwig Göransson"),
        ],
    },
    {
        "name": "Best Original Song",
        "order": 13,
        "nominees": [
            ("Dear Me", "Diane Warren: Relentless"),
            ("Golden", "KPop Demon Hunters"),
            ("I Lied To You", "Sinners"),
            ("Sweet Dreams Of Joy", "Viva Verdi!"),
            ("Train Dreams", "Train Dreams"),
        ],
    },
    {
        "name": "Best Cinematography",
        "order": 14,
        "nominees": [
            ("Frankenstein", "Dan Laustsen"),
            ("Marty Supreme", "Darius Khondji"),
            ("One Battle after Another", "Michael Bauman"),
            ("Sinners", "Autumn Durald Arkapaw"),
            ("Train Dreams", "Adolpho Veloso"),
        ],
    },
    {
        "name": "Best Film Editing",
        "order": 15,
        "nominees": [
            ("F1", "Stephen Mirrione"),
            ("Marty Supreme", "Ronald Bronstein & Josh Safdie"),
            ("One Battle after Another", "Andy Jurgensen"),
            ("Sentimental Value", "Olivier Bugge Coutté"),
            ("Sinners", "Michael P. Shawver"),
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
