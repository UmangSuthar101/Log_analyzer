from collections import Counter,defaultdict

def analyze_logs(parsed_logs):
    from datetime import datetime

    total_logs = len(parsed_logs)
    levels = Counter(log["level"] for log in parsed_logs)
    user_counts = Counter(log["user_id"] for log in parsed_logs)
    top_users = user_counts.most_common(3)
    failed_actions = sum(1 for log in parsed_logs if log["status"] == "failed")
    timestamps = [log["timestamp"] for log in parsed_logs]
    first_log_time = min(timestamps)
    last_log_time = max(timestamps)
    action_breakdown = Counter(log["action"] for log in parsed_logs)
    per_hour_logs = Counter(log["timestamp"].strftime("%Y-%m-%d %H:00") for log in parsed_logs)


    return {
        "total_logs": total_logs,
        "levels": dict(levels),
        "top_users": [{"user_id": uid, "count": count} for uid,count in top_users],
        "failed_actions": failed_actions,
        "first_log_time": first_log_time.isoformat(),
        "last_log_time": last_log_time.isoformat(),
        "action_breakdown": dict(action_breakdown),
        "per_hour_logs": dict(per_hour_logs),
    }