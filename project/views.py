# Standard Library
import logging
import os
import subprocess

# Django
from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import render

log = logging.getLogger(__name__)


def _is_sync_allowed():
    """Check if database sync is allowed.

    Only permitted when:
    - Not running in production (settings.prod)
    - BARBERSCORE_PROD_DATABASE env var is set
    """
    is_prod = settings.DJANGO_SETTINGS_MODULE == 'settings.prod'
    has_source = bool(os.environ.get('BARBERSCORE_PROD_DATABASE'))
    return (not is_prod) and has_source


def sync_prod_db_confirm(request):
    """Show confirmation page before syncing production database."""
    if not _is_sync_allowed():
        return HttpResponseForbidden("Database sync is not available in this environment.")
    return render(request, 'admin/sync_prod_db_confirm.html')


def sync_prod_db_execute(request):
    """Execute the production database sync after confirmation."""
    if request.method != 'POST':
        return HttpResponseForbidden("POST required.")
    if not _is_sync_allowed():
        return HttpResponseForbidden("Database sync is not available in this environment.")
    if not request.POST.get('confirmed'):
        return HttpResponseForbidden("Confirmation required.")

    prod_db_url = os.environ['BARBERSCORE_PROD_DATABASE']
    local_db_url = os.environ['DATABASE_URL']

    # Step 1: pg_dump | pg_restore
    restore_cmd = 'pg_dump -Fc "{prod}" | pg_restore --clean --if-exists --no-owner -n public -d "{local}"'.format(
        prod=prod_db_url,
        local=local_db_url,
    )
    try:
        restore_result = subprocess.run(
            restore_cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=600,  # 10 minute timeout
        )
        restore_output = (restore_result.stdout + restore_result.stderr).strip()
        restore_ok = restore_result.returncode == 0
    except subprocess.TimeoutExpired:
        restore_output = "ERROR: pg_dump/pg_restore timed out after 10 minutes."
        restore_ok = False
    except Exception as e:
        restore_output = "ERROR: {e}".format(e=e)
        restore_ok = False

    # Step 2: migrate (only if restore succeeded)
    if restore_ok:
        try:
            migrate_result = subprocess.run(
                ['django-admin', 'migrate', '--noinput'],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
            )
            migrate_output = (migrate_result.stdout + migrate_result.stderr).strip()
            migrate_ok = migrate_result.returncode == 0
        except subprocess.TimeoutExpired:
            migrate_output = "ERROR: migrate timed out after 5 minutes."
            migrate_ok = False
        except Exception as e:
            migrate_output = "ERROR: {e}".format(e=e)
            migrate_ok = False
    else:
        migrate_output = "Skipped (restore failed)."
        migrate_ok = False

    success = restore_ok and migrate_ok
    if success:
        log.info("Production database sync completed successfully.")
    else:
        log.error("Production database sync failed.")

    context = {
        'success': success,
        'restore_output': restore_output or '(no output)',
        'migrate_output': migrate_output or '(no output)',
    }
    return render(request, 'admin/sync_prod_db_result.html', context)
