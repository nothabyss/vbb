import time

timestamp = time.time()
local_time = time.localtime(timestamp)

hour = local_time.tm_hour
minute = local_time.tm_min
second = local_time.tm_sec

print(f"Current time：{hour}h {minute}min {second}sec")