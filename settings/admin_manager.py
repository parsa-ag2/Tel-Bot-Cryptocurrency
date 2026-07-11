from database.db import SessionLocal
from database.models import Admin
from config import OWNER_ID


# =========================
# Add Admin
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
# =========================

def get_admins():

    db = SessionLocal()

    try:

        return (
            db.query(Admin)
            .all()
        )


    except Exception as e:

        print(
            f"Get admins error: {e}"
        )

        return []


    finally:

        db.close()



# =========================
# Check Admin
# =========================

def is_admin(
    telegram_id: int
):

    try:
        owner = int(OWNER_ID)

    except:

        owner = OWNER_ID


    # مالک اصلی همیشه دسترسی دارد
    if telegram_id == owner:
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


    except Exception as e:

        print(
            f"Check admin error: {e}"
        )

        return False


    finally:

        db.close()