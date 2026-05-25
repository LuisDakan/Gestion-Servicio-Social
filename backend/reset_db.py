"""Reset database — keeps only the admin user."""
import sys
sys.path.insert(0, "/app")

from app.database import SessionLocal
from app.models.user import User
from app.services.auth_service import hash_password
from sqlalchemy import text

db = SessionLocal()

try:
    db.execute(text("DELETE FROM solicitudes"))
    db.execute(text("DELETE FROM vacantes"))
    db.execute(text("DELETE FROM password_reset_tokens"))
    db.execute(text("DELETE FROM sessions"))
    db.execute(text("DELETE FROM alumnos"))
    db.execute(text("DELETE FROM empresas"))
    db.execute(text("DELETE FROM carreras"))
    db.execute(text("DELETE FROM users"))
    db.commit()

    admin = User(
        name="Admin",
        email="admin@test.com",
        username="admin",
        password=hash_password("admin"),
        role="admin",
    )
    db.add(admin)
    db.commit()

    print("Database reset successfully!")
    print(f"  Admin: admin / admin")

except Exception as e:
    db.rollback()
    print(f"Error: {e}")
    sys.exit(1)
finally:
    db.close()
