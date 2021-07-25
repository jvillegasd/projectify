import redis
from environs import Env
from rq import Worker, Queue, Connection

env = Env()
env.read_env()

listen = ['docs']
conn = redis.from_url(env('REDIS_URL'))

if __name__ == '__main__':
  with Connection(conn):
    worker = Worker(map(Queue, listen))
    worker.work()
