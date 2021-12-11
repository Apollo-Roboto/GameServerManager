import enum

class Status(enum.Enum):
	STARTING=0
	RUNNING=1
	FAILED=2
	STOPPED=3