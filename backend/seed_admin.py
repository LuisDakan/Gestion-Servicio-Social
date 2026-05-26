from app.database import SessionLocal
from app.models.user import User
from app.services.auth_service import hash_password


def seed_admin():
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.username == "admin").first():
            admin = User(
                name="Admin",
                email="admin@ss.unam.mx",
                username="admin",
                password=hash_password("admin"),
                role="admin",
            )
            db.add(admin)
            db.commit()
            print("✓ Admin user created (admin / admin)")
        else:
            print("✓ Admin user already exists")
    finally:
        db.close()


if __name__ == "__main__":
    seed_admin()
