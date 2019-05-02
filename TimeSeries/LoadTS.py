import redis, time, random

r = redis.Redis('localhost', 6379, socket_timeout=10)

#r.execute_command('TS.CREATE', 'test-ts', 'retention', '60', 'labels', 'name', 'test')
 
start = time.time()
end = start + 10
#while time.time() < end:
while True:
    r.execute_command('TS.ADD', 'test-ts', '*', random.uniform(0, 10))
    time.sleep(0.5)
