from queue import PriorityQueue
import itertools

priority_map = {
    "critical": 1,
    "high": 2,
    "normal": 3,
    "low": 4
}

notification_queue = PriorityQueue()

# unique counter to avoid comparison issue
counter = itertools.count()