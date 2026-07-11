from database.db import SessionLocal
from database.models import Admin
from config import OWNER_ID


# =========================
# Add Admin
# اضافه کردن ادمین
# =========================

def add_admin(
    telegram_id: int,
    username: str = None,
    added_by: int = None
):

    db = SessionLocal()

    try:

        exists = (
            db.query(Admin)
            .filter(
                Admin.telegram_id == telegram_id
            )
            .first()
        )


        if exists:
            return False


        admin = Admin(
            telegram_id=telegram_id,
            username=username,
            added_by=added_by
        )


        db.add(admin)
        db.commit()

        return True


    except Exception as e:

        db.rollback()
        print(
            f"Add admin error: {e}"
        )

        return False


    finally:

        db.close()



# =========================
# Remove Admin
# حذف ادمین
# =========================

def remove_admin(
    telegram_id: int
):

    db = SessionLocal()

    try:

        admin = (
            db.query(Admin)
            .filter(
                Admin.telegram_id == telegram_id
            )
            .first()
        )


        if not admin:
            return False


        db.delete(admin)

        db.commit()

        return True


    except Exception as e:

        db.rollback()

        print(
            f"Remove admin error: {e}"
        )

        return False


    finally:

        db.close()



# =========================
# Get Admin List
# لیست ادمین ها
# =========================

def get_admins():

    db = SessionLocal()

    try:

        admins = (
            db.query(Admin)
            .all()
        )

        return admins


    finally:

        db.close()



# =========================
# Check Admin
# بررسی ادمین بودن
# =========================

def is_admin(telegram_id: int):

    # مالک اصلی همیشه ادمین است
    if telegram_id == OWNER_ID:
        return True


    db = SessionLocal()

    try:

        admin = (
            db.query(Admin)
            .filter(
                Admin.telegram_id == telegram_id
            )
            .first()
        )

        return admin is not None


    finally:

        db.close()