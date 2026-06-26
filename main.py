from monitoring import SystemMonitor, print_message
from config import HOST,USER,ignore_fs,LOG_PATH, LOG_FILE, SERVICES, PORTS
import os, subprocess

def display_menu():
    print("*" * 33)
    print(f"* {'SRE MONITORING TOOL':^30}*")
    print("*" * 33)
    print(f"* {'1. Disk Usage Check':<30}*")
    print(f"* {'2. Memory Usage Check':<30}*")
    print(f"* {'3. CPU Usage Check':<30}*")
    print(f"* {'4. TOP CPU Processes':<30}*")
    print(f"* {'5. Service Status Check':<30}*")
    print(f"* {'6. Port Check':<30}*")
    print(f"* {'7. Load Average Check':<30}*")
    print(f"* {'8. Run Full Health Check':<30}*")
    print(f"* {'9. Exit':<30}*")
    print("*" * 33)

    ch = input("Enter your choice: ")
    return ch

"""Check SSH Connectivity"""
def validate_ssh_connectivity():
    command = ["ssh", "-o", "ConnectTimeout=5", f"{USER}@{HOST}", "echo CONNECTED"]
    ssh_output = subprocess.run(command, capture_output=True, text=True)

    if not ssh_output.stdout.strip() == "CONNECTED":
        return False
    return True

###-----MAIN------###
"""Initialize class"""
healthcheck = SystemMonitor(HOST, USER)

connection_status = validate_ssh_connectivity()
if not connection_status:
    print("SSH Connectivity Failed")
    exit()

#--Check if log path exists--#
healthcheck.check_dir(LOG_PATH)

#---Check if log folder and file exists in local system---#
log_dir = os.path.expanduser(LOG_PATH)
log_file = os.path.join(log_dir, LOG_FILE)
os.makedirs(log_dir, exist_ok=True)
if not os.path.isfile(log_file):
    with open(file=log_file, mode='w') as log:
        log.write("")

while True:
    choice = display_menu()
    print("\n")
    with open(file=log_file, mode="a") as log:
        message = "STARTING HEALTH CHECK"
        print_message(message, log, data_flag='N')

        if choice == "1":
            healthcheck.check_disk(ignore_fs, log)
        elif choice == "2":
            healthcheck.check_memory(log)
        elif choice == "3":
            healthcheck.check_cpu(log)
        elif choice == "4":
            healthcheck.top_cpu_process(log)
        elif choice == "5":
            healthcheck.check_service_status(SERVICES, log)
        elif choice == "6":
            healthcheck.check_port(PORTS, log)
        elif choice == "7":
            healthcheck.load_average(log)
        elif choice == "8":
            message = "RUNNING FULL HEALTH CHECK"
            print_message(message, log, data_flag='N')
            healthcheck.check_disk(ignore_fs, log)
            healthcheck.check_memory(log)
            healthcheck.check_cpu(log)
            healthcheck.top_cpu_process(log)
            healthcheck.check_service_status(SERVICES, log)
            healthcheck.check_port(PORTS, log)
            healthcheck.load_average(log)
            message = "HEALTH CHECK COMPLETED"
            print_message(message, log, data_flag='N')
        elif choice == "9":
            message = "EXITING THE HEALTH CHECK"
            print_message(message, log, data_flag='N')
            output = healthcheck.file_transfer(LOG_PATH, LOG_FILE)
            if output == 0:
                message = "File Transferred Successfully"
            else:
                message = "File Transferred Failed"

            print_message(message, log, data_flag='N')
            break
        else:
            print("Invalid Choice. Please try again")



