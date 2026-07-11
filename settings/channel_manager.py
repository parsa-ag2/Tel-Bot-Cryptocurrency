from database.db import SessionLocal
from database.models import RequiredChannel



# =========================
# Add Channel
# افزودن کانال اجباری
# =========================

def add_channel(
    channel_id: int,
    username: str = None,
    title: str = None
):

    db = SessionLocal()

    try:

        exists = (
            db.query(RequiredChannel)
            .filter(
                RequiredChannel.channel_id == channel_id
            )
            .first()
        )


        if exists:
            return False


        channel = RequiredChannel(
            channel_id=channel_id,
            username=username,
            title=title
        )


        db.add(channel)
        db.commit()

        return True


    except Exception as e:

        db.rollback()

        print(
            f"Add channel error: {e}"
        )

        return False


    finally:

        db.close()



# =========================
# Remove Channel
# حذف کانال
# =========================

def remove_channel(
    channel_id: int
):

    db = SessionLocal()

    try:

        channel = (
            db.query(RequiredChannel)
            .filter(
                RequiredChannel.channel_id == channel_id
            )
            .first()
        )


        if not channel:
            return False


        db.delete(channel)

        db.commit()

        return True


    except Exception as e:

        db.rollback()

        print(
            f"Remove channel error: {e}"
        )

        return False


    finally:

        db.close()



# =========================
# Get Channels
# لیست کانال ها
# =========================

def get_channels():

    db = SessionLocal()

    try:

        channels = (
            db.query(RequiredChannel)
            .filter(
                RequiredChannel.is_active == True
            )
            .all()
        )


        return channels


    finally:

        db.close()



# =========================
# Get Channel IDs
# برای چک عضویت کاربر
# =========================

def get_channel_ids():

    db = SessionLocal()

    try:

        channels = (
            db.query(RequiredChannel.channel_id)
            .filter(
                RequiredChannel.is_active == True
            )
            .all()
        )


        return [
            channel[0]
            for channel in channels
        ]


    finally:

        db.close()



# =========================
# Check Channel Exists
# =========================

def channel_exists(
    channel_id: int
):

    db = SessionLocal()

    try:

        channel = (
            db.query(RequiredChannel)
            .filter(
                RequiredChannel.channel_id == channel_id
            )
            .first()
        )


        return channel is not None


    finally:

        db.close()



# =========================
# Enable / Disable Channel
# فعال یا غیرفعال کردن
# =========================

def toggle_channel(
    channel_id: int,
    status: bool
):

    db = SessionLocal()

    try:

        channel = (
            db.query(RequiredChannel)
            .filter(
                RequiredChannel.channel_id == channel_id
            )
            .first()
        )


        if not channel:
            return False


        channel.is_active = status

        db.commit()

        return True


    except Exception as e:

        db.rollback()

        print(
            f"Toggle channel error: {e}"
        )

        return False


    finally:

        db.close()