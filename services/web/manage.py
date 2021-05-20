from datetime import datetime
from flask.cli import FlaskGroup

from project import app, db, Email


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    email1 = Email(
        from_email="team@vuemastery.com",
        subject="What's up with Vue 3.0? Here's how to find out from Evan You",
        body="The opening keynote of VueConf US this year was Evan You (the creator of Vue), giving his State of the Vuenion address. He walked us through the journey of getting Vue 3 from a prototype to a reality the past year. He also dove into Vue's overall growth in the community.",
        sent_at=datetime(2021, 3, 27, 18, 45, 43))

    email2 = Email(
        from_email="jeffrey@vuetraining.com",
        subject="Learn by doing Vue 3 Zero to Intermediate in 8 weeks",
        body="Building projects is one of the most effective ways to learn - and _the_ most effective way _remember_ what you've learned - but it can be frustrating.\n\nThis 8-week course takes the pain out of 'learning by doing'.\n\nEach week we give you\n\n* a project that will grow your skills without overwhelming you\n* links to hand-picked resources, such as Vue Mastery videos, that share the knowledge you'll need for the project (no more useless rabbit holes)\n* answers to any and all questions you have while working\n* feedback on your completed code (so you're only learning good habits)\n\nOur instructors are standing by to answer your questions.\n\nReady to learn?",
        sent_at=datetime(2021, 5, 20, 18, 25, 43))

    email3 = Email(
        from_email="damian@dulisz.com",
        subject="#177: Updated Vue.js Roadmap; Vuex v4.0.0-alpha.1 has been released; Kia King Ishii join the core team; Nuxt v2.12 released; Videos from Vue.js Amsterdam 2020 are here!",
        body="First of all, lets congratulate Kia King Ishii on joining the Vue.js core team! 🎉 He has been doing an incredible job building vuex-orm and will now focus on working on the next versions of Vuex.\n\nSpeaking of which – Vuex v4.0.0-alpha.1 has just been released! This is the version of Vuex that will work with Vue 3.0 but keep the familiar API you know from the current version.",
        sent_at=datetime(2021, 3, 18, 18, 25, 43))

    email4 = Email(
        from_email="anthony@vuejsdevelopers.com",
        subject="'Vue 3 Release Roadmap' + 6 more must-read articles from this week",
        body="Newsletter Issue #161",
        sent_at=datetime(2021, 3, 24, 18, 25, 43))

    db.session.add_all([email1, email2, email3, email4])
    db.session.commit()


if __name__ == "__main__":
    cli()
