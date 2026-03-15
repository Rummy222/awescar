"""Seed the database with 98th Academy Awards nominees (2026 ceremony)."""
from app import app
from models import db, Category, Nominee, Prediction, Setting

CATEGORIES = [
    {
        "name": "Best Animated Short Film",
        "order": 1,
        "nominees": [
            ("Butterfly", "Florence Miailhe & Ron Dyens"),
            ("Forevergreen", "Nathan Engelhardt & Jeremy Spears"),
            ("The Girl Who Cried Pearls", "Chris Lavis & Maciek Szczerbowski"),
            ("Retirement Plan", "John Kelly & Andrew Freedman"),
            ("The Three Sisters", "Konstantin Bronzit"),
        ],
    },
    {
        "name": "Best Live Action Short Film",
        "order": 2,
        "nominees": [
            ("Butcher's Stain", "Meyer Levinson-Blount & Oron Caspi"),
            ("A Friend of Dorothy", "Lee Knight & James Dean"),
            ("Jane Austen's Period Drama", "Julia Aks & Steve Pinder"),
            ("The Singers", "Sam A. Davis & Jack Piatt"),
            ("Two People Exchanging Saliva", "Alexandre Singh & Natalie Musteata"),
        ],
    },
    {
        "name": "Best Documentary Short Film",
        "order": 3,
        "nominees": [
            ("All the Empty Rooms", "Joshua Seftel & Conall Jones"),
            ("Armed Only with a Camera", "Craig Renaud & Juan Arredondo"),
            ("Children No More: \"Were and Are Gone\"", "Hilla Medalia & Sheila Nevins"),
            ("The Devil Is Busy", "Christalyn Hampton & Geeta Gandbhir"),
            ("Perfectly a Strangeness", "Alison McAlpine"),
        ],
    },
    {
        "name": "Best Documentary Feature Film",
        "order": 4,
        "nominees": [
            ("The Alabama Solution", ""),
            ("Come See Me in the Good Light", ""),
            ("Cutting through Rocks", ""),
            ("Mr. Nobody against Putin", ""),
            ("The Perfect Neighbor", ""),
        ],
    },
    {
        "name": "Best International Feature Film",
        "order": 5,
        "nominees": [
            ("The Secret Agent", "Brazil"),
            ("It Was Just an Accident", "France"),
            ("Sentimental Value", "Norway"),
            ("Sirāt", "Spain"),
            ("The Voice of Hind Rajab", "Tunisia"),
        ],
    },
    {
        "name": "Best Animated Feature Film",
        "order": 6,
        "nominees": [
            ("Arco", "Ugo Bienvenu, Félix de Givry & Natalie Portman"),
            ("Elio", "Madeline Sharafian & Domee Shi"),
            ("KPop Demon Hunters", "Maggie Kang & Chris Appelhans"),
            ("Little Amélie or the Character of Rain", "Maïlys Vallade"),
            ("Zootopia 2", "Jared Bush & Byron Howard"),
        ],
    },
    {
        "name": "Best Original Score",
        "order": 7,
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
        "order": 8,
        "nominees": [
            ("Dear Me", "Diane Warren: Relentless"),
            ("Golden", "KPop Demon Hunters"),
            ("I Lied To You", "Sinners"),
            ("Sweet Dreams Of Joy", "Viva Verdi!"),
            ("Train Dreams", "Train Dreams"),
        ],
    },
    {
        "name": "Best Sound",
        "order": 9,
        "nominees": [
            ("F1", "Gareth John, Al Nelson & Gwendolyn Yates Whittle"),
            ("Frankenstein", "Greg Chapman, Nathan Robitaille & Nelson Ferreira"),
            ("One Battle after Another", "José Antonio García & Christopher Scarabosio"),
            ("Sinners", "Chris Welcker, Benjamin A. Burtt & Felipe Pacheco"),
            ("Sirāt", "Amanda Villavieja, Laia Casanovas & Yasmina Praderas"),
        ],
    },
    {
        "name": "Best Visual Effects",
        "order": 10,
        "nominees": [
            ("Avatar: Fire and Ash", "Joe Letteri, Richard Baneham & Eric Saindon"),
            ("F1", "Ryan Tudhope, Nicolas Chevallier & Robert Harrington"),
            ("Jurassic World Rebirth", "David Vickery, Stephen Aplin & Charmaine Chan"),
            ("The Lost Bus", "Charlie Noble, David Zaretti & Russell Bowen"),
            ("Sinners", "Michael Ralla, Espen Nordahl & Guido Wolter"),
        ],
    },
    {
        "name": "Best Makeup and Hairstyling",
        "order": 11,
        "nominees": [
            ("Frankenstein", "Mike Hill, Jordan Samuel & Cliona Furey"),
            ("Kokuho", "Kyoko Toyokawa, Naomi Hibino & Tadashi Nishimatsu"),
            ("Sinners", "Ken Diaz, Mike Fontaine & Shunika Terry"),
            ("The Smashing Machine", "Kazu Hiro, Glen Griffin & Bjoern Rehbein"),
            ("The Ugly Stepsister", "Thomas Foldberg & Anne Cathrine Sauerberg"),
        ],
    },
    {
        "name": "Best Costume Design",
        "order": 12,
        "nominees": [
            ("Avatar: Fire and Ash", "Deborah L. Scott"),
            ("Frankenstein", "Kate Hawley"),
            ("Hamnet", "Malgosia Turzanska"),
            ("Marty Supreme", "Miyako Bellizzi"),
            ("Sinners", "Ruth E. Carter"),
        ],
    },
    {
        "name": "Best Production Design",
        "order": 13,
        "nominees": [
            ("Frankenstein", "Tamara Deverell & Shane Vieau"),
            ("Hamnet", "Fiona Crombie & Alice Felton"),
            ("Marty Supreme", "Jack Fisk & Adam Willis"),
            ("One Battle after Another", "Florencia Martin & Anthony Carlino"),
            ("Sinners", "Hannah Beachler & Monique Champagne"),
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
    {
        "name": "Best Casting",
        "order": 16,
        "nominees": [
            ("Hamnet", "Nina Gold"),
            ("Marty Supreme", "Jennifer Venditti"),
            ("One Battle after Another", "Cassandra Kulukundis"),
            ("The Secret Agent", "Gabriel Domingues"),
            ("Sinners", "Francine Maisler"),
        ],
    },
    {
        "name": "Best Adapted Screenplay",
        "order": 17,
        "nominees": [
            ("Bugonia", "Will Tracy"),
            ("Frankenstein", "Guillermo del Toro"),
            ("Hamnet", "Chloé Zhao & Maggie O'Farrell"),
            ("One Battle after Another", "Paul Thomas Anderson"),
            ("Train Dreams", "Clint Bentley & Greg Kwedar"),
        ],
    },
    {
        "name": "Best Original Screenplay",
        "order": 18,
        "nominees": [
            ("Blue Moon", "Robert Kaplow"),
            ("It Was Just an Accident", "Jafar Panahi"),
            ("Marty Supreme", "Ronald Bronstein & Josh Safdie"),
            ("Sentimental Value", "Eskil Vogt & Joachim Trier"),
            ("Sinners", "Ryan Coogler"),
        ],
    },
    {
        "name": "Best Supporting Actor",
        "order": 19,
        "nominees": [
            ("Benicio Del Toro", "One Battle after Another"),
            ("Jacob Elordi", "Frankenstein"),
            ("Delroy Lindo", "Sinners"),
            ("Sean Penn", "One Battle after Another"),
            ("Stellan Skarsgård", "Sentimental Value"),
        ],
    },
    {
        "name": "Best Supporting Actress",
        "order": 20,
        "nominees": [
            ("Elle Fanning", "Sentimental Value"),
            ("Inga Ibsdotter Lilleaas", "Sentimental Value"),
            ("Amy Madigan", "Weapons"),
            ("Wunmi Mosaku", "Sinners"),
            ("Teyana Taylor", "One Battle after Another"),
        ],
    },
    {
        "name": "Best Actor",
        "order": 21,
        "nominees": [
            ("Timothée Chalamet", "Marty Supreme"),
            ("Leonardo DiCaprio", "One Battle after Another"),
            ("Ethan Hawke", "Blue Moon"),
            ("Michael B. Jordan", "Sinners"),
            ("Wagner Moura", "The Secret Agent"),
        ],
    },
    {
        "name": "Best Actress",
        "order": 22,
        "nominees": [
            ("Jessie Buckley", "Hamnet"),
            ("Rose Byrne", "If I Had Legs I'd Kick You"),
            ("Kate Hudson", "Song Sung Blue"),
            ("Renate Reinsve", "Sentimental Value"),
            ("Emma Stone", "Bugonia"),
        ],
    },
    {
        "name": "Best Director",
        "order": 23,
        "nominees": [
            ("Chloé Zhao", "Hamnet"),
            ("Josh Safdie", "Marty Supreme"),
            ("Paul Thomas Anderson", "One Battle after Another"),
            ("Joachim Trier", "Sentimental Value"),
            ("Ryan Coogler", "Sinners"),
        ],
    },
    {
        "name": "Best Picture",
        "order": 24,
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
]


def seed():
    """Upsert categories and nominees — existing IDs are preserved so predictions persist."""
    with app.app_context():
        db.create_all()

        for cat_data in CATEGORIES:
            # Find or create category by name (preserves ID)
            cat = Category.query.filter_by(name=cat_data["name"]).first()
            if not cat:
                cat = Category(name=cat_data["name"])
                db.session.add(cat)
            cat.display_order = cat_data["order"]
            db.session.flush()

            # Build lookup of existing nominees for this category
            existing = {n.name: n for n in cat.nominees}
            seed_names = {name for name, _ in cat_data["nominees"]}

            # Update or create nominees
            for name, detail in cat_data["nominees"]:
                if name in existing:
                    existing[name].detail = detail  # update detail in case it changed
                else:
                    db.session.add(Nominee(category_id=cat.id, name=name, detail=detail))

            # Remove nominees no longer in the list, only if no predictions reference them
            for name, nominee in existing.items():
                if name not in seed_names:
                    has_predictions = Prediction.query.filter_by(nominee_id=nominee.id).first()
                    if not has_predictions:
                        db.session.delete(nominee)

        if not db.session.get(Setting, "predictions_locked"):
            db.session.add(Setting(key="predictions_locked", value="false"))

        db.session.commit()
        print(f"Seeded/updated {len(CATEGORIES)} categories.")


if __name__ == "__main__":
    seed()
