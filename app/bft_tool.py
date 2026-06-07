import subprocess
from datetime import datetime
from pathlib import Path
import time
from collections.abc import Callable

from app.bft_constants import BFT_TESTS, BFT_SPECS, PDA_CONFIGS

class BFTTool:
    def __init__(self, serial_no: str):
        
        # Gets current month and day
        today_path = datetime.now().strftime('%m/%d')
        
        self.serial_no = serial_no.strip()
        
        # Define directories
        self.base_dir = Path(f'/home/admin/Desktop/sstc/test-results/bft/{self.serial_no}/{today_path}')
        
        # Shared paths
        self.hostfile = "/tarana/images/rn0"
        
        self._process: subprocess.Popen | None = None

    def build_t3_cmd(self, sub_dir: str, script: str, args: str = "") -> str:
        out_path = f"{self.base_dir}/{sub_dir}"
        args_str = f"-- {args}" if args else ""
        return f"t3 devicetest --force --output {out_path} -H {self.hostfile} {script} {args_str}"

    def _build_pda_args(self, band: str) -> str:
        cfg = PDA_CONFIGS[band]
        return (
            f"--fixture_loss_c0={cfg['fixture_loss_c0']} "
            f"--fixture_loss_c1={cfg['fixture_loss_c1']}"
        )

    def get_commands(self) -> dict[str, str]:
        """Maps each test name to its t3 command."""
        commands = {}
        for test_name, spec in BFT_SPECS.items():
            args = spec.get("args", "")
            if spec.get("args_type") == "pda":
                args = self._build_pda_args(spec["band"])

            commands[test_name] = self.build_t3_cmd(
                spec["sub_dir"],
                spec["script"],
                args,
            )

        return commands
        
    def run_selected(self, selected: list[str], on_result: Callable[[dict], None]):
        commands = self.get_commands()
        
        for name in selected:
            cmd = commands[name]

            on_result({
                "name": name,
                "command": cmd,
                "status": "running",
                "duration": None,
                "output_path": str(self.base_dir / name)
            })

            start = time.time()
            self._process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = self._process.communicate()
            returncode = self._process.returncode
            duration = round(time.time() - start, 1)

            # Debug prints
            print(f"--- {name} ---")
            print(f"returncode: {returncode}")
            print(f"stdout: {stdout.decode()}")
            print(f"stderr: {stderr.decode()}")

            if returncode is None:
                break

            on_result({
                "name": name,
                "command": cmd,
                "status": "pass" if returncode == 0 else "fail",
                "duration": duration,
                "output_path": str(self.base_dir / name)
            })

        # After all tests are done, reset the process reference
        # If stop() were somehow called after the run finishes, it could attempt to terminate a process that already ended
        self._process = None

    def stop(self):
        
        # self._process.poll() checks if the process has already finished. 
        # returns None   → process is still running
        # returns 0      → process finished successfully
        # returns 1      → process finished with an error
        
        # Terminating an already-finished process would crash your program, so we have to check if it's still running before trying to stop it.
        if self._process and self._process.poll() is None:
            self._process.terminate()