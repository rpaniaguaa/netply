import subprocess

def get_interfaces():
    args = ["ls","/sys/class/net/"]
    command = subprocess.run(args,capture_output=True,text=True)
    return command.stdout.strip()

a = get_interfaces()
print(a)
