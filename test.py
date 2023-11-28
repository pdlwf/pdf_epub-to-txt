import threading
import queue
import time

def producer(progress_queue):
    for i in range(1, 101):
        message = f"<{i * 10}ms: {i}%>"
        progress_queue.put(message)
        time.sleep(0.01)  # 暂停10毫秒
        print(message,1000000)

def consumer(progress_queue):
    time.sleep(0.1)  # 暂停100毫秒
    while True:
        time.sleep(0.01)  # 暂停100毫秒
        try:
            message = progress_queue.get(timeout=0.01)  # 尝试在10毫秒内从队列获取消息
            print(message, 200000)
        except queue.Empty:
            print("已经冒有数据了@")
            break  # 如果队列为空，则退出循环

# 创建队列
progress_queue = queue.Queue()

# 创建并启动生产者和消费者线程
producer_thread = threading.Thread(target=producer, args=(progress_queue,))
consumer_thread = threading.Thread(target=consumer, args=(progress_queue,))

producer_thread.start()
consumer_thread.start()

# 等待线程完成
producer_thread.join()
consumer_thread.join()
