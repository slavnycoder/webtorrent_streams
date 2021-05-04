from django.conf import settings

broker_url = settings.REDIS_URL

timezone = settings.TIME_ZONE
enable_utc = True

beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'
task_ignore_result = True
worker_hijack_root_logger = True

task_routes = {
                  'streams.tasks.*': {'queue': 'streams'},
              },
