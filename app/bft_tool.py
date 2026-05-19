import subprocess
from datetime import datetime
from pathlib import Path
import time
from collections.abc import Callable

AVAILABLE_TESTS = [
    "cal_set_freq_test",
    "rf_init_g2_rn_3ghz",
    "mfg_pda_g2_rn_3ghz",
    "rf_init_g2_rn_6ghz",
    "mfg_pda_g2_rn_6ghz",
]

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

    def get_commands(self) -> dict[str, str]:
        """Maps each test name to its t3 command."""
        return {
            "cal_set_freq_test" : self.build_t3_cmd("cal_set_freq_test", "/usr/local/ntf/system/cal_set_freq_test.ntf"),
            "rf_init_g2_rn_3ghz": self.build_t3_cmd("rf_init_g2_rn_3ghz", "/usr/local/ntf/qa/rf/system/mfg_ntfs/rf_init_g2_rn_3ghz.ntf"),
            "mfg_pda_g2_rn_3ghz": self.build_t3_cmd("mfg_pda_g2_rn_3ghz", "/usr/local/ntf/qa/rf/pda/mfg_pda_g2_rn_3ghz.ntf", "--fixture_loss_c0=8.09,8.43,8.80,8.57,8.53,8.14,8.11,8.02 --fixture_loss_c1=8.17,8.58,8.11,8.61,8.72,8.28,8.22,8.14"),
            "rf_init_g2_rn_6ghz": self.build_t3_cmd("rf_init_g2_rn_6ghz", "/usr/local/ntf/qa/rf/system/mfg_ntfs/rf_init_g2_rn_6ghz.ntf"),
            "mfg_pda_g2_rn_6ghz": self.build_t3_cmd("mfg_pda_g2_rn_6ghz", "/usr/local/ntf/qa/rf/pda/mfg_pda_g2_rn_6ghz.ntf", "--fixture_loss_c0=11.8,11.75,11.78,11.34,11.69,11.32,11.48,11.58 --fixture_loss_c1=10.77,11.03,11.21,10.73,10.76,10.9,11.11,11.15"),
        }
        
        # return {
        #     "cal_set_freq_test" : "sleep 1",
        #     "rf_init_g2_rn_3ghz": "sleep 2",
        #     "mfg_pda_g2_rn_3ghz": "sleep 3",
        #     "rf_init_g2_rn_6ghz": "sleep 4",
        #     "mfg_pda_g2_rn_6ghz": "sleep 5",
        # }
        
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