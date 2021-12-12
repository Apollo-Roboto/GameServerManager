from datetime import datetime
from time import sleep
import random
import sys

def log(s):
	print(f"[{datetime.now().isoformat()}] : {s}")
	sys.stdout.flush()

for _ in range(5):
	log(f"Preparing something ({_})")
	sleep(random.random())

log("Server is ready to serve !!!")

for _ in range(25):
	log(f"Doing something ({_})")
	sleep(random.random())