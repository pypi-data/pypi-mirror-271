import subprocess
import sys


def build_project(*args):
    if not args:
        args = ["-w"]

    process = subprocess.run([sys.executable, "-m", "build", *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if process.returncode:
        raise Exception(process.stderr.decode("utf-8"))
