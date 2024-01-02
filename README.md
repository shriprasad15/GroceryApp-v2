

-> final order of commands
 -> `npm i` (frontend)
  -> run the app `python app.py`
  -> `celery -A backjobs worker -l info`
  -> `celery -A backjobs beat -l info`


[//]: # (pip install -U kaleido)
