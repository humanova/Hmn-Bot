import subprocess

def evaluate_command(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(f"evaluating {cmd}...")

    output = str
    for line in p.stdout.readlines():
        output += line.decode('utf-8')
    return_val = p.wait()

    return output
