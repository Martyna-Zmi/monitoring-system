import json
import random
import time
from datetime import datetime, timezone

file_path = "/shared/metrics.json"

while True:
    metrics = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "cpu": random.randint(0, 100),
            "ram": random.randint(0, 100),
            "disk": random.randint(0, 100)
    }
    with open(file_path, "w+") as f:
        json.dump(metrics, f)
    print("generated data successfully")
    time.sleep(10)
