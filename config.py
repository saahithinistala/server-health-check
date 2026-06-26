USER = "myuser"
HOST = "xxx.xx.xx.x"
ignore_fs = ["tmpfs", "devtmpfs", "udev", "overlay", "none"]
LOG_PATH = "~/sre-monitoring/logs"
LOG_FILE = "system_health_check.log"
SERVICES = [
    "ssh",
    "systemd-journald",
    "systemd-resolved",
    "cron",
    "snap.microk8s.daemon-kubelite",
    "snap.microk8s.daemon-k8s-dqlite"
]
PORTS = {"SSH": 22, "HTTP": 80, "HTTPS": 443}

