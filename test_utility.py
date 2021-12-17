from datetime import datetime
from time import sleep
import random
import sys

def delay():
	sleep(random.random()*2)

def log(s):
	print(f"[{datetime.now().isoformat()}] : {s}")
	sys.stdout.flush()

for _ in range(5):
	log(f"Preparing something ({_})")
	delay()

log("Server is ready to serve !!!")

for _ in range(50):
	log(f"Doing something ({_})")
	delay()