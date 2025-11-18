from celery import Celery

from src.redis_db import REDIS_URL

celery = Celery(
    main="tasks",
    broker=REDIS_URL,
 )
