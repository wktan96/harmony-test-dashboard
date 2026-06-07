import subprocess
import time
from pathlib import Path
from collections.abc import Callable

from app.dvt_constants import DVT_FLOWS, TEST_SPECS, RF_INIT_ARGS, PDA_CONFIGS

TEMPERATURE_OPTIONS = {
    "25c":  25,
    "60c":  60,
    "-45c": -45,
}

# Re-export for backward compatibility
DVT_TESTS = [test for tests in DVT_FLOWS.values() for test in tests]


class DVTTool:
    def __init__(self, serial_no: str, temperature: str):
        self.serial_no  = serial_no.strip()
        self.temp_str   = temperature
        self.temp_input = TEMPERATURE_OPTIONS[temperature]

        self.base_dir = Path(f"/home/admin/Desktop/sstc/test-results/dvt/{self.serial_no}/{self.temp_str}")
        self.dir_3g   = self.base_dir / "3g"
        self.dir_6g   = self.base_dir / "6g"
        self.hostfile = "/tarana/images/rn0"
        self.pathloss = "/tarana/images/sanmina_dvt_pathloss.json"

        self._process: subprocess.Popen | None = None

    def _build_t3_cmd(self, band_dir: Path, flow: str, sub_dir: str, script: str, args: str = "") -> str:
        out_path = f"{band_dir}_{flow}/{sub_dir}"
        return f"t3 devicetest --force --output {out_path} -H {self.hostfile} {script} -- {args}"

    def _build_pda_args(self, variant: str) -> str:
        """Build PDA test arguments from config."""
        cfg = PDA_CONFIGS[variant]
        return (
            f"--fixture_loss_c0={cfg['fixture_loss_c0']} "
            f"--fixture_loss_c1={cfg['fixture_loss_c1']} "
            f"--carrier_freqs={cfg['carrier_freqs']} --mech_atten=0 --skip_eeprom_write "
            f"--nulling_start_atten=99 --temperature_log={self.temp_input} "
            f"-L={cfg['power_levels']}"
        )

    def _get_band_dir(self, band: str) -> Path:
        """Get the base directory for a band."""
        return self.dir_3g if band == "3g" else self.dir_6g

    def get_commands(self) -> dict[str, str]:
        """Generate all test commands from parametrized specs."""
        # Calculate reference paths
        refs = {
            "tx_gain_ref_3g": f"{self.dir_3g}_tf3/tx_gain_3g/RFDVT_TxGain-test_Tx_Gain",
            "rx_gain_ref_3g": f"{self.dir_3g}_tf5/rx_gain_nf_3g/Rx_GainNF-test_Rx_GainNF",
            "tx_gain_ref_6g": f"{self.dir_6g}_tf3/tx_gain_6g/RFDVT_TxGain-test_Tx_Gain",
            "rx_gain_ref_6g": f"{self.dir_6g}_tf5/rx_gain_nf_6g/Rx_GainNF-test_Rx_GainNF",
        }

        commands = {}
        for test_name, spec in TEST_SPECS.items():
            band_dir = self._get_band_dir(spec["band"])
            flow = spec["flow"]
            sub_dir = spec["sub_dir"]
            script = spec["script"]

            # Determine arguments
            if "args" in spec:
                # Direct args with template substitution
                args = spec["args"].format(temp=self.temp_input, pathloss=self.pathloss, **refs)
            elif spec.get("args_type") == "rf_init_3g":
                args = f"{RF_INIT_ARGS['3g']} {spec.get('args_extra', '')}"
            elif spec.get("args_type") == "rf_init_6g":
                args = f"{RF_INIT_ARGS['6g']} {spec.get('args_extra', '')}"
            elif spec.get("args_type") == "pda_3g":
                args = self._build_pda_args(spec["pda_variant"])
            elif spec.get("args_type") == "pda_6g":
                args = self._build_pda_args(spec["pda_variant"])
            else:
                args = ""

            commands[test_name] = self._build_t3_cmd(band_dir, flow, sub_dir, script, args)

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
                "output_path": None,
            })

            start = time.time()
            self._process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = self._process.communicate()
            returncode = self._process.returncode
            duration = round(time.time() - start, 1)

            if returncode is None:
                break

            on_result({
                "name": name,
                "command": cmd,
                "status": "pass" if returncode == 0 else "fail",
                "duration": duration,
                "output_path": None,
            })

        self._process = None
        
    def get_test_flow(self,test_name: str) -> str:
        """Returns the flow name for a given test name."""
        for flow_name, tests in DVT_FLOWS.items():
            if test_name in tests:
                return flow_name
        return "Unknown"

    def stop(self):
        if self._process and self._process.poll() is None:
            self._process.terminate()