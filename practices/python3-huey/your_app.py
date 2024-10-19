from huey import RedisHuey
from huey import crontab
#from huey import put
#import pprint
import os

# Initialize Huey
huey = RedisHuey('my_app', host='redis', port=6379)

print(os.getpid())

@huey.task()
def add(a, b):
    print(os.getpid())
    result = a + b
    huey.put("result",result)


if __name__ == "__main__":
    # Enqueue a task
    result = add(3, 4)
    print(f"Task enqueued, result: {result}")
    print(f"Task enqueued, result: {vars(result)}")
    result = add(3, 8)
    print(f"Task enqueued, result: {result}")
    print(f"Task enqueued, result: {vars(result)}")
