#!/usr/bin/env python3
import subprocess
import time

def check_ping(host):
    """Pings a host once. Returns True if up, False if down."""
    try:
        # -c 1: 1 packet, -W 2: 2-second timeout
        command = ["ping", "-c", "1", "-W", "2", host]
        result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0
    except Exception:
        return False

if __name__ == "__main__":
    # Target to monitor (e.g., waiting for a rebooting server to come online)
    target_host = "192.168.12.2"
    delay_seconds = 2  # Time to wait between failed ping attempts
    
    print(f"Monitoring {target_host}. Waiting for response...")
    
    attempt = 1
    while True:
        if check_ping(target_host):
            print(f"\n Success! {target_host} responded on attempt {attempt}.")
            print("Stopping ping test.")
            break  # This exits the loop immediately
        else:
            print(f" Attempt {attempt}: Host is still down. Retrying in {delay_seconds}s...", end="\r")
            attempt += 1
            time.sleep(delay_seconds)
