import time
from jugaad_data.nse import bhavcopy_save

def backfill(dates, destination, max_cons_errors = 10):
    failed = []
    consecutive = 0
    for d in dates:
        try:
            bhavcopy_save(d, destination)
            consecutive = 0
        except Exception as e:
            failed.append((d, type(e).__name__, str(e)))
            print(d, type(e).__name__, e)
            consecutive += 1
            if consecutive >= max_cons_errors:
                print(f'Stopping: {max_cons_errors} errors in a row ending at {d}')
                break
        time.sleep(1)
    return failed