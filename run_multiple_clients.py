import argparse
import subprocess
import sys

def run_clients(num_clients, ip, port, file):
    processes = []

    for _ in range(num_clients):
        # Start each client.py process
        process = subprocess.Popen(['python3', 'client.py', '-i', ip, '-p', str(port), '-f', file])
        processes.append(process)
        print(f"Started client process with PID: {process.pid}")

    # Wait for all processes to complete
    for process in processes:
        process.wait()
        print(f"Client process with PID {process.pid} has completed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--count", type=int, required=True, help="Number of clients")
    parser.add_argument("-i", "--ip", type=str, required=True, help="Server\'s IP address")
    parser.add_argument("-p", "--port", type=int, required=True, help="Server\'s port")
    parser.add_argument("-f", "--file", type=str, required=True, help="Client\'s input file")

    try:
        args = parser.parse_args()

    except SystemExit as e:
        parser.print_help()
        sys.exit()

    run_clients(args.count, args.ip, args.port, args.file)