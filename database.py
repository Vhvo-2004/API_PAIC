import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import socket

DATABASE_URL = os.getenv("DATABASE_URL")
print("DEBUG =>", repr(DATABASE_URL))  # debug seguro

url = os.getenv("DATABASE_URL")
print("URL =", repr(url))
try:
    host = url.split("@")[1].split(":")[0]
    print("Attempting DNS resolution for:", host)
    print("Resolved:", socket.gethostbyname(host))
except Exception as e:
    print("DNS RESOLUTION ERROR:", e)


engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
