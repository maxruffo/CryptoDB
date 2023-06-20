import json
import os
import threading
from datetime import datetime, timedelta


"""from datetime import datetime,timedelta


end_date = datetime.now()
print(end_date)"""




"""yesterday = datetime.now() - timedelta(days=1)
start_date = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
end_date = start_date + timedelta(days=1)


print(start_date)
print(end_date)



import os"""

num_threads = os.cpu_count()
print("Anzahl der verfügbaren Threads:", num_threads)
