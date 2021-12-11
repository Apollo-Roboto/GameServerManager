from datetime import datetime
from time import sleep
import random
import sys

def log(s):
	print(f"[{datetime.now().isoformat()}] : {s}")
	sys.stdout.flush()

for _ in range(10):
	log("Preparing something")
	sleep(random.random())

log("Server is ready to serve !!!")

for _ in range(10):
	log("Doing something")
	sleep(random.random())