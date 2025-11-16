import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

print("DEBUG => DATABASE_URL =", repr(os.getenv("DATABASE_URL")))
DATABASE_URL = os.getenv("postgresql://postgreespaic_user:lPCsscFQFH4E6PROLWz50fUHm839w7CV@dpg-d4d0br8gjchc73dmj2u0-a/postgreespaic")  # será INTERNAL_URL no Render

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
