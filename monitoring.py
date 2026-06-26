import os.path
import subprocess
from datetime import datetime

def get_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def print_message(print_msg, logfile, data_flag):
    timestamp = get_timestamp()

    if data_flag == "N":
        print_msg = f'<-----{timestamp}: {print_msg}----->\n'

    print(print_msg)
    logfile.write(print_msg)


class SystemMonitor:

    def __init__(self, host, username):
        self.host = host
        self.username = username

    def check_dir(self, log_path):
        command = (f'ssh {self.username}@{self.host} "test -d {log_path} || '
                   f'(mkdir -p {log_path} && echo Log directory created successfully)"')
        output = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(f"{output.stdout}")

    def file_transfer(self, log_path, file):
        log_dir = os.path.expanduser(log_path)
        command = f'scp {log_dir}/{file} {self.username}@{self.host}:{log_path}/{file}'
        output = subprocess.run(command, shell=True, capture_output=True, text=True)
        return output.returncode

    def check_disk(self, ignore_fs, file):
        message = "DISK SPACE CHECK"
        print_message(message, file, data_flag='N')
        command = f'ssh {self.username}@{self.host} "df -h"'
        output = subprocess.run(command, shell=True, capture_output=True, text=True)
        result = output.stdout

        for data in result.splitlines()[1:]:
            parts = data.split()
            fs = parts[0]
            used = parts[4]
            used_perc = int(used.split("%")[0])
            mounted = parts[5]

            if len(parts) < 5:
                continue

            status = ""
            if fs not in ignore_fs:
                if used_perc <= 70:
                    status = "OK"
                elif 70 < used_perc <= 85:
                    status = "WARNING"
                elif used_perc > 85:
                    status = "CRITICAL"

                message = f"Filesystem: {fs}\nMount Point: {mounted}\nUsed: {used}\nStatus: {status}\n\n"
                print_message(message, file, data_flag='Y')

    def check_memory(self, file):
        message = "MEMORY USAGE CHECK"
        print_message(message, file, data_flag='N')
        command = f'ssh {self.username}@{self.host} "free -m | grep Mem"'
        output = subprocess.run(command, shell=True, capture_output=True, text=True)

        for data in output.stdout.splitlines():
            parts = data.split()
            total_memory = int(parts[1])
            used_memory = int(parts[2])
            free_memory = int(parts[3])
            memory_use_perc = round((used_memory / total_memory) * 100, 2)

            status = ""
            if memory_use_perc <= 70:
                status = "OK"
            elif 70 < memory_use_perc <= 85:
                status = "WARNING"
            elif memory_use_perc > 85:
                status = "CRITICAL"

            message = (f"Total Memory: {total_memory} MB\nUsed Memory: {used_memory} MB\n"
                       f"Free Memory: {free_memory} MB\nUsed Percentage: {memory_use_perc}\nStatus: {status}\n\n")
            print_message(message, file, data_flag='Y')

    def check_cpu(self, file):
        message = "CPU USAGE CHECK"
        print_message(message, file, data_flag='N')
        command = f'ssh {self.username}@{self.host} "top -bn1 | grep Cpu"'
        output = subprocess.run(command, shell=True, capture_output=True, text=True)
        result = output.stdout.split(",")
        idle_cpu = float(result[3].strip().split()[0])
        cpu_idle_perc = 100 - round(idle_cpu, 2)

        status = ""
        if cpu_idle_perc <= 70:
            status = "OK"
        elif 70 < cpu_idle_perc <= 85:
            status = "WARNING"
        elif cpu_idle_perc > 85:
            status = "CRITICAL"

        message = f"CPU Usage: {round(cpu_idle_perc, 2)}%\nStatus: {status}"
        print_message(message, file, data_flag='Y')
        print("\n")

    def top_cpu_process(self, file):
        message = "TOP CPU PROCESSES"
        print_message(message, file, data_flag='N')
        command = f'ssh {self.username}@{self.host} "ps -eo pid,comm,%cpu --sort=-%cpu | head -6"'
        output = subprocess.run(command, shell=True, capture_output=True, text=True)
        message = output.stdout
        print_message(message, file, data_flag='Y')

    def check_service_status(self, services_list, file):
        message = "SERVICE STATUS"
        print_message(message, file, data_flag='N')
        for service in services_list:
            command = f'ssh {self.username}@{self.host} "systemctl is-active {service}"'
            output = subprocess.run(command, text=True, capture_output=True, shell=True)
            output = output.stdout.strip()
            message = f'{service: <35} {output.upper()}'
            print_message(message, file, data_flag='Y')
        print("\n")

    def check_port(self, ports, file):
        message = "PORT STATUS"
        print_message(message, file, data_flag='N')
        print(f"{'Service':<9}{'Port':<5}{'Status'}")
        print(f"{'-' * 7:<9}{'-' * 4:<5}{'-'* 6}")
        for key, value in ports.items():
            command = f'ssh {self.username}@{self.host} "ss -tuln | grep -w :{value}"'
            output = subprocess.run(command, shell=True, capture_output=True, text=True)

            if output.returncode == 0:
                status = "LISTENING"
            else:
                status = "NOT LISTENING"

            message = f"{key:<9}{value:<5}{status}"
            print_message(message, file, data_flag='Y')
        print("\n")

    def load_average(self, file):
        message = "LOAD AVERAGE"
        print_message(message, file, data_flag='N')
        command = f'ssh {self.username}@{self.host} "uptime"'
        output = subprocess.run(command, shell=True, capture_output=True, text=True)
        load_avg = output.stdout.split(",")[3:]
        one_min_load = (load_avg[0]).split(':')[1].strip()
        five_min_load = load_avg[1].strip()
        fifteen_min_load = load_avg[2].strip()

        if float(one_min_load) <= 1:
            status = "OK"
        elif 1 < float(one_min_load) < 2:
            status = "WARNING"
        else:
            status = "CRITICAL"

        message = f"{'1 Minute ':<12}: {one_min_load}\n{'5 Minutes':<12}: {five_min_load}\n{'15 Minutes':<12}: {fifteen_min_load}\n{'Status':<12}: {status}"
        print_message(message, file, data_flag='Y')
        print("\n")









