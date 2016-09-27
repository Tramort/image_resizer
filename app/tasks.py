from ImageResizer.celery_test import app
from datetime import timedelta

@app.task(bind=True)
def test(self):
    print("is works!")