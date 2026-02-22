# ============================================================
# HOTFIX — OPS-410: Disk Filling Up — Logs Not Rotating
# Priority: P1 | SLA: 30 minutes | Reporter: Ops Alert
# ============================================================
#
# The log rotation is broken. Logs grow indefinitely and disk
# fills up every 3 days. The rotation function has bugs.
#
# ============================================================

import os
from datetime import datetime

class LogRotator:
    def __init__(self, log_dir='./logs', max_size_mb=10, max_files=5):
        self.log_dir = log_dir
        self.max_size_mb = max_size_mb
        self.max_files = max_files

    def should_rotate(self, filepath):
        if not os.path.exists(filepath):
            return False
        # Needs to convert: size_bytes / (1024 * 1024) > max_size_mb
        size = os.path.getsize(filepath)
        return size > self.max_size_mb  # Compares bytes to MB!

    def rotate(self, filepath):
        if not self.should_rotate(filepath):
            return False

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        rotated = f'{filepath}.{timestamp}'
        os.rename(filepath, rotated)

        self._cleanup_old_files(filepath)
        return True

    def _cleanup_old_files(self, base_path):
        log_dir = os.path.dirname(base_path) or '.'
        base_name = os.path.basename(base_path)
        rotated = sorted([
            f for f in os.listdir(log_dir)
            if f.startswith(base_name + '.')
        ])
        while len(rotated) >= self.max_files:
            old = rotated.pop(0)
                      os.path.join(log_dir, old + '.old'))

if __name__ == '__main__':
    rotator = LogRotator(max_size_mb=10)
    print(f'Should rotate (10 bytes assumed): {rotator.should_rotate(__file__)}')
