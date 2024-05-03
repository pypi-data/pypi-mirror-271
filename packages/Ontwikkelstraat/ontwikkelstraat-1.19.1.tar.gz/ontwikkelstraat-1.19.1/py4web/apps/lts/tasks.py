"""
To use celery tasks:
1) pip install -U "celery[redis]" 
2) In settings.py: 
   USE_CELERY = True
   CELERY_BROKER = "redis://localhost:6379/0"
3) Start "redis-server"
4) Start "celery -A apps.{appname}.tasks beat"
5) Start "celery -A apps.{appname}.tasks worker --loglevel=info" for each worker

Retries, see http://www.ines-panker.com/2020/10/29/retry-celery-tasks.html

"""
import getpass

from pydal import DAL
from pydal.validators import CRYPT

from .common import fragmentx_scheduler as scheduler

# from edwh.core.backend.ntfy_sh import error, warning
# from ycecream import y
# from attrs import define, field
Row = DAL.Row


# # example of task that needs db access


# @scheduler.task
# def my_task():
#     try:
#         # this task will be executed in its own thread, connect to db
#         db._adapter.reconnect()
#         # do something here
#         db.commit()
#     except:
#         # rollback on failure
#         db.rollback()


@scheduler.task
def log_once(who=None):
    # usage: log_once.delay()

    # this task will be executed in its own thread, connect to db
    # db._adapter.reconnect()

    if not who:
        who = "World"
    print(f"Hello {who}")


def add_lts_admin_user(email: str):
    # dc exec py4web py4web call apps lts.tasks.add_lts_admin_user --args '{"email": "robin@educationwarehouse.nl"}'
    from .common_lts import lts_users_db
    from .models_lts import groups

    user = lts_users_db.auth_user(email=email)

    if not user:
        print("User does not exist, creating new user.")
        password = getpass.getpass("Please choose a password: ")

        password_secure = CRYPT()(password)[0]

        user_id = lts_users_db.auth_user.insert(
            email=email,
            password=password_secure,
        )

        user = lts_users_db.auth_user(user_id)

    if "admin" in (existing_groups := groups.get(user.id)):
        print("User is already admin!", existing_groups)
        return

    print(f"Making {user.first_name} ({user.id}) admin")
    groups.add(user.id, "admin")

    lts_users_db.commit()

# @scheduler.task
# def log_often():
#     print("Hello Again")
#
# # run my_task every 10 seconds
# scheduler.conf.beat_schedule = {
#     "my_first_task": {
#         "task": "apps.%s.tasks.log_often" % settings.APP_NAME,
#         "schedule": 10.0,
#         "args": (),
#     },
# }
