"""
lo2
====
test.py
"""
from datetime import datetime, timedelta

class YourClass:
    """ YourClass"""
    def __init__(self):
        self.timeformat = '%S.%f'

    def time_diff(self, start: str, end: str) -> float:
        """
        计算两个时间戳的差值
        Args:
            start: 开始时间
            end: 结束时间
        Returns:
            时间差（秒）
        """
        start_datetime = datetime.strptime(start, self.timeformat)
        end_datetime = datetime.strptime(end, self.timeformat)

        # Convert milliseconds to microseconds
        millisecond_difference = (end_datetime - start_datetime).total_seconds() * 1000
        microseconds_difference = int(millisecond_difference) * 1000

        return microseconds_difference / 1e6  # Convert microseconds to seconds

# Example usage
your_instance = YourClass()
start_time = '70.854436'
end_time = '72.123456'
time_difference = your_instance.time_diff(start_time, end_time)
print(time_difference)
