from app import create_app


app = create_app()


with app.app_context():
    # Import here to avoid circular imports during module import-time
    from app import db
    from app.models import Admin

    username = input("Admin username: ").strip()
    email = input("Admin email: ").strip()
    password = input("Admin password: ")

    existing = Admin.query.filter_by(username=username).first()

    if existing:
        print("Admin already exists.")
    else:
        admin = Admin(username=username, email=email)
        admin.set_password(password)

        db.session.add(admin)
        db.session.commit()

        print("Admin account created successfully.")