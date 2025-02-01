import logging
import sys

import psutil


class ResourceUsageFilter(logging.Filter):
    def filter(self, record):
        process = psutil.Process()
        mem_info = process.memory_info()
        cpu_percent = psutil.cpu_percent(interval=0.1)
        record.memory_used = mem_info.rss / (1024 * 1024)
        record.cpu_percent = cpu_percent
        return True


class SafeFormatter(logging.Formatter):
    def format(self, record):
        process = psutil.Process()
        mem_info = process.memory_info()
        cpu_percent = psutil.cpu_percent(interval=0.1)
        if not hasattr(record, "memory_used"):
            record.memory_used = mem_info.rss / (1024 * 1024)
        if not hasattr(record, "cpu_percent"):
            record.cpu_percent = cpu_percent
        return super().format(record)


formatter = SafeFormatter(
    "%(asctime)s,%(msecs)d [Memory: %(memory_used) 7.3f MB] [CPU: %(cpu_percent) 6.3f%%] "
    "[process id: %(process)d] [Thread: %(thread)d] [Name: %(name)s] [Level: %(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.addFilter(ResourceUsageFilter())