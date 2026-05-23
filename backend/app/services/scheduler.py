from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal
from app.services.solicitud_service import expirar_aceptaciones_vencidas


def expiry_job():
    db = SessionLocal()
    try:
        count = expirar_aceptaciones_vencidas(db)
        if count:
            print(f"[scheduler] Expired {count} stale acceptances")
    except Exception as e:
        print(f"[scheduler] Error: {e}")
    finally:
        db.close()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(expiry_job, "interval", seconds=60)
    scheduler.start()
