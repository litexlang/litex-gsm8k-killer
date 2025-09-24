import multiprocessing as mp
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from killer import killer
from utils.http_utils import get_task_list


MAX_PROCESSORS = 100

task_list = get_task_list(length=20)

with mp.Pool(processes=MAX_PROCESSORS) as pool:
    results = pool.map(killer, task_list)

success_count = 0
failure_count = 0

for res in results:
    if res["solution"] == None:
        failure_count += 1
    else:
        success_count += 1

print(f"Total tasks processed: {len(results)}")
print(f"Successful solutions: {success_count}")
print(f"Failed solutions: {failure_count}")

# Total tasks processed: 20
# Successful solutions: 18
# Failed solutions: 2