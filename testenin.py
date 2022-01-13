import time
import sys

for _ in range(10):
	print("hello")
	sys.stdout.flush()
	time.sleep(1)

print("server ready")

for _ in range(10):
	print("hello")
	sys.stdout.flush()
	time.sleep(1)