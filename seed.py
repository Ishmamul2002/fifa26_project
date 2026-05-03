from app import create_app, db
from app.models import User, Team

app = create_app()

with app.app_context():
    # ==================== USER ====================
    user = User.query.filter_by(email='user@fifa26.com').first()
    
    if user:
        user.set_password("password123")
        db.session.commit()
        print("✅ Password reset for existing user!")
    else:
        new_user = User(
            username="Admin User",
            email="user@fifa26.com",
            country="Bangladesh",
            is_admin=True
        )
        new_user.set_password("password123")
        db.session.add(new_user)
        db.session.commit()
        print("✅ New test user created!")

    print("Email: user@fifa26.com")
    print("Password: password123")

    # ==================== TEAMS (48 Teams with Flags) ====================
    teams_data = [
        {"name": "Argentina", "country": "Argentina", "flag": "🇦🇷", "group_name": "A"},
        {"name": "Brazil", "country": "Brazil", "flag": "🇧🇷", "group_name": "A"},
        {"name": "France", "country": "France", "flag": "🇫🇷", "group_name": "B"},
        {"name": "Germany", "country": "Germany", "flag": "🇩🇪", "group_name": "B"},
        {"name": "Spain", "country": "Spain", "flag": "🇪🇸", "group_name": "C"},
        {"name": "England", "country": "England", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "group_name": "C"},
        {"name": "Portugal", "country": "Portugal", "flag": "🇵🇹", "group_name": "D"},
        {"name": "Belgium", "country": "Belgium", "flag": "🇧🇪", "group_name": "D"},
        {"name": "Netherlands", "country": "Netherlands", "flag": "🇳🇱", "group_name": "E"},
        {"name": "Italy", "country": "Italy", "flag": "🇮🇹", "group_name": "E"},
        {"name": "Croatia", "country": "Croatia", "flag": "🇭🇷", "group_name": "F"},
        {"name": "Uruguay", "country": "Uruguay", "flag": "🇺🇾", "group_name": "F"},
        {"name": "Algeria", "country": "Algeria", "flag": "🇩🇿", "group_name": "G"},
        {"name": "Australia", "country": "Australia", "flag": "🇦🇺", "group_name": "G"},
        {"name": "Canada", "country": "Canada", "flag": "🇨🇦", "group_name": "H"},
        {"name": "Chile", "country": "Chile", "flag": "🇨🇱", "group_name": "H"},
        {"name": "Morocco", "country": "Morocco", "flag": "🇲🇦", "group_name": "A"},
        {"name": "Japan", "country": "Japan", "flag": "🇯🇵", "group_name": "B"},
        {"name": "South Korea", "country": "South Korea", "flag": "🇰🇷", "group_name": "C"},
        {"name": "Mexico", "country": "Mexico", "flag": "🇲🇽", "group_name": "D"},
        {"name": "USA", "country": "United States", "flag": "🇺🇸", "group_name": "E"},
        {"name": "Senegal", "country": "Senegal", "flag": "🇸🇳", "group_name": "F"},
        {"name": "Nigeria", "country": "Nigeria", "flag": "🇳🇬", "group_name": "G"},
        {"name": "Egypt", "country": "Egypt", "flag": "🇪🇬", "group_name": "H"},
        {"name": "Saudi Arabia", "country": "Saudi Arabia", "flag": "🇸🇦", "group_name": "A"},
        {"name": "Iran", "country": "Iran", "flag": "🇮🇷", "group_name": "B"},
        {"name": "Qatar", "country": "Qatar", "flag": "🇶🇦", "group_name": "C"},
        {"name": "Tunisia", "country": "Tunisia", "flag": "🇹🇳", "group_name": "D"},
        {"name": "Poland", "country": "Poland", "flag": "🇵🇱", "group_name": "E"},
        {"name": "Denmark", "country": "Denmark", "flag": "🇩🇰", "group_name": "F"},
        {"name": "Switzerland", "country": "Switzerland", "flag": "🇨🇭", "group_name": "G"},
        {"name": "Sweden", "country": "Sweden", "flag": "🇸🇪", "group_name": "H"},
        # You can add more teams here if you want
    ]

    added_count = 0
    for data in teams_data:
        existing = Team.query.filter_by(name=data["name"]).first()
        if not existing:
            team = Team(**data)
            db.session.add(team)
            added_count += 1
            print(f"✅ Added: {data['name']} {data['flag']}")

    db.session.commit()
    print(f"\n🎉 Seeding completed! {added_count} new teams added.")
    print(f"Total teams in database: {Team.query.count()}")