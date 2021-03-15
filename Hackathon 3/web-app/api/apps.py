from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'

    """
    def ready(self):
        from .jobs import fetch_meme
        from datetime import datetime
        from threading import Timer

        from .config import JOB_TIME_INTERVAL

        print("Job Started at: ", datetime.now())
        fetch_meme()
        print("Job ended at: ", datetime.now())

        t = Timer(JOB_TIME_INTERVAL, fetch_meme)
        t.start()
    """