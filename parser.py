import re
from datetime import datetime

log_pattern = re.compile(r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\s+'
                         r'(?P<level>\w+)\s+user_id=(?P<user_id>\d+)\s+action=(?P<action>\w+)\s+status=(?P<status>\w+)')

def parse_log_line(line):
    match = log_pattern.match(line)
    if match:
        data = match.groupdict()
        data["timestamp"] = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S,%f")
        return data
    return None