from huey import RedisHuey
from huey import crontab

# Initialize Huey
huey = RedisHuey('my_app', host='redis', port=6379)

@huey.task()
def add(a, b):
    return a + b

if __name__ == "__main__":
    # Enqueue a task
    result = add(3, 4)
    print(f"Task enqueued, result: {result}")
