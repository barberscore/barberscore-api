import os
import json
from redis import Redis
from rq import Queue
from rq.job import Job
from rq.exceptions import NoSuchJobError
from rq.registry import DeferredJobRegistry
from rq.registry import FailedJobRegistry
from rq.registry import FinishedJobRegistry
from rq.registry import ScheduledJobRegistry
from rq.registry import StartedJobRegistry

# Connect using Heroku's environment variable
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
# Heroku Redis uses self-signed certificates on rediss:// connections,
# so skip certificate verification (same as settings/base.py).
if redis_url.startswith('rediss://'):
    redis_conn = Redis.from_url(redis_url, ssl_cert_reqs=None)
else:
    redis_conn = Redis.from_url(redis_url)

# Queues to export (matches RQ_QUEUES in settings)
queue_names = ['default', 'high', 'low']

# Registries to export alongside the pending jobs
registry_classes = {
    'started': StartedJobRegistry,
    'scheduled': ScheduledJobRegistry,
    'deferred': DeferredJobRegistry,
    'finished': FinishedJobRegistry,
    'failed': FailedJobRegistry,
}


def serialize_job(job, status):
    data = {
        "id": job.id,
        "status": status,
        "origin": job.origin,
        "created_at": str(job.created_at),
        "enqueued_at": str(job.enqueued_at),
        "started_at": str(job.started_at),
        "ended_at": str(job.ended_at),
        "description": job.description,
        "kwargs": {k: str(v) for k, v in (job.kwargs or {}).items()},
        "args": [str(arg) for arg in (job.args or [])],
    }
    if job.exc_info:
        data["exc_info"] = job.exc_info
    return data


exported_jobs = []
counts = {}

for queue_name in queue_names:
    q = Queue(queue_name, connection=redis_conn)

    # Jobs currently pending in the queue
    for job in q.jobs:
        exported_jobs.append(serialize_job(job, 'pending'))
        counts['{0}/pending'.format(queue_name)] = counts.get(
            '{0}/pending'.format(queue_name), 0) + 1

    # Jobs in the queue's registries (failed, started, etc.)
    for status, registry_class in registry_classes.items():
        registry = registry_class(queue=q)
        for job_id in registry.get_job_ids():
            try:
                job = Job.fetch(job_id, connection=redis_conn)
            except NoSuchJobError:
                # Job data expired or was deleted; keep the id at least
                exported_jobs.append({"id": job_id, "status": status, "origin": queue_name})
                continue
            exported_jobs.append(serialize_job(job, status))
            counts['{0}/{1}'.format(queue_name, status)] = counts.get(
                '{0}/{1}'.format(queue_name, status), 0) + 1

# Save to a JSON file
with open('rq_export.json', 'w') as f:
    json.dump(exported_jobs, f, indent=4)

print("Successfully exported {0} jobs:".format(len(exported_jobs)))
for key in sorted(counts):
    print("  {0}: {1}".format(key, counts[key]))
