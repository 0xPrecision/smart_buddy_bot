from datetime import datetime
import os

import peewee as pw


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "memebase.db")

# Инициализация базы данных SQLite
db = pw.SqliteDatabase(db_path)


class BaseModel(pw.Model):
    """
    Base model for all project tables.
    
    Attributes:
    Meta.database (peewee.Database): Reference to the database object.
	"""

    class Meta:
        database = db


class User(BaseModel):
    """
    Model for a Telegram bot user.
    
    Attributes:
    telegram_id (int): Unique Telegram user ID.
	"""

    telegram_id = pw.IntegerField(unique=True)


class Analysis(BaseModel):
    """
    Model for analyzing a user's wallet.
    
    Attributes:
    user (User): Reference to the user (foreign key).
    wallet_address (str): Solana wallet address.
    nickname (str): Wallet nickname set by the user.
    created_at (datetime): Date and time when the analysis was created.
    result (str): Text result of the analysis (e.g., transaction report).
	"""

    user = pw.ForeignKeyField(User, backref="analyses")
    wallet_address = pw.CharField()
    nickname = pw.CharField()
    created_at = pw.DateTimeField(default=datetime.now)
    result = pw.TextField()
