import base64
import datetime
import os
from io import BytesIO

import ujson
from apscheduler.triggers.date import DateTrigger
from nonebot import scheduler
from sqlitedict import SqliteDict


def get_path(*paths):
    return os.path.join(os.path.dirname(__file__), *paths)


def pil2b64(data):
    bio = BytesIO()
    data = data.convert("RGB")
    data.save(bio, format="JPEG", quality=75)
    base64_str = base64.b64encode(bio.getvalue()).decode()
    return "base64://" + base64_str


def cancel_call_later(job_id):
    scheduler.remove_job(job_id, "default")


def call_later(delay, func, job_id):
    if scheduler.get_job(job_id, "default"):
        cancel_call_later(job_id)
    now = datetime.datetime.now()
    notify_time = now + datetime.timedelta(seconds=delay)
    return scheduler.add_job(
        func,
        trigger=DateTrigger(notify_time),
        id=job_id,
        misfire_grace_time=60,
        coalesce=True,
        jobstore="default",
        max_instances=1,
    )


db = {}


def init_db(db_dir="db", db_name="db.sqlite", tablename="unnamed") -> SqliteDict:
    if db.get(db_name):
        return db[db_name]
    db[db_name] = SqliteDict(
        get_path(db_dir, db_name),
        tablename=tablename,
        encode=ujson.dumps,
        decode=ujson.loads,
        autocommit=True,
    )
    return db[db_name]
