"""DVT test definitions and command specifications.

This module contains:
- DVT_FLOWS: Test flow organization
- TEST_SPECS: Data-driven test configuration for command generation
- Command argument templates and builders
"""

from app.config import DEV_MODE

# Test flow organization
DVT_FLOWS = {
    "3GHz Test Flow 1": [
        "tx_rf_init_cont_tx_3g_tf1",
        "tx_freq_align_3g_tf1",
        "tx_pda_low_3g",
        "tx_pda_mid_3g",
        "tx_pda_high_3g",
        "tx_ant_iso_3g",
        "tx_pa_noise_3g",
        "tx_vcxo_3g",
    ],
    "3GHz Test Flow 2": [
        "tx_rf_init_cont_tx_3g_tf2",
        "tx_freq_align_3g_tf2",
        "tx_npr_vs_freq_sep_3g",
        "tx_pd_vs_pwr_freq_3g",
    ],
    "3GHz Test Flow 3": [
        "tx_rf_init_cont_tx_3g_tf3",
        "tx_freq_align_3g_tf3",
        "tx_gain_3g",
        "tx_phase_noise_3g",
    ],
    "3GHz Test Flow 4": [
        "tx_rf_init_txcal_3g",
        "tx_cal_path_3g",
        "tx_cal_iso_3g",
    ],
    "3GHz Test Flow 5": [
        "rx_rf_init_rxcal_3g_tf5",
        "rx_freq_align_3g",
        "rx_gain_nf_3g",
        "rx_iip3_inband_3g",
        "rx_ant_iso_3g",
        "rx_iq_freq_sel_3g",
    ],
    "3GHz Test Flow 6": [
        "rx_rf_init_rxcal_3g_tf6",
        "rx_cal_path_3g",
        "rx_cal_iso_3g",
    ],
    "6GHz Test Flow 1": [
        "tx_rf_init_cont_tx_6g_tf1",
        "tx_freq_align_6g_tf1",
        "tx_pda_low_unii34",
        "tx_pda_mid_unii34",
        "tx_pda_high_unii34",
        "tx_pda_low_unii5",
        "tx_pda_mid_unii5",
        "tx_pda_high_unii5",
        "tx_pda_low_unii7",
        "tx_pda_mid_unii7",
        "tx_pda_high_unii7",
        "tx_ant_iso_6g",
        "tx_pa_noise_6g",
        "tx_vcxo_6g",
    ],
    "6GHz Test Flow 2": [
        "tx_rf_init_cont_tx_6g_tf2",
        "tx_freq_align_6g_tf2",
        "tx_npr_vs_freq_sep_6g",
        "tx_pd_vs_pwr_freq_6g",
    ],
    "6GHz Test Flow 3": [
        "tx_rf_init_cont_tx_6g_tf3",
        "tx_freq_align_6g_tf3",
        "tx_gain_6g",
        "tx_phase_noise_6g",
    ],
    "6GHz Test Flow 4": [
        "tx_rf_init_txcal_6g",
        "tx_cal_path_6g",
        "tx_cal_iso_6g",
    ],
    "6GHz Test Flow 5": [
        "rx_rf_init_rxcal_6g_tf5",
        "rx_freq_align_6g",
        "rx_gain_nf_6g",
        "rx_iip3_inband_6g",
        "rx_ant_iso_6g",
        "rx_iq_freq_sel_6g",
    ],
    "6GHz Test Flow 6": [
        "rx_rf_init_rxcal_6g_tf6",
        "rx_cal_path_6g",
        "rx_cal_iso_6g",
    ],
}

PRESET_3GHZ_REDUCED = {
    "3GHz Test Flow 1": [
        "tx_rf_init_cont_tx_3g_tf1",
        "tx_freq_align_3g_tf1",
        "tx_pda_low_3g",
        "tx_pda_mid_3g",
        "tx_pda_high_3g",
        "tx_ant_iso_3g",
    ],
    "3GHz Test Flow 3": [
        "tx_rf_init_cont_tx_3g_tf3",
        "tx_freq_align_3g_tf3",
        "tx_gain_3g",
    ],
    "3GHz Test Flow 4": [
        "tx_rf_init_txcal_3g",
        "tx_cal_path_3g",
        "tx_cal_iso_3g",
    ],
    "3GHz Test Flow 5": [
        "rx_rf_init_rxcal_3g_tf5",
        "rx_freq_align_3g",
        "rx_gain_nf_3g",
        "rx_ant_iso_3g",
    ],
    "3GHz Test Flow 6": [
        "rx_rf_init_rxcal_3g_tf6",
        "rx_cal_path_3g",
        "rx_cal_iso_3g",
    ],
}

PRESET_6GHZ_REDUCED = {
    "6GHz Test Flow 1": [
        "tx_rf_init_cont_tx_6g_tf1",
        "tx_freq_align_6g_tf1",
        "tx_pda_low_unii34",
        "tx_pda_mid_unii34",
        "tx_pda_high_unii34",
        "tx_pda_low_unii5",
        "tx_pda_mid_unii5",
        "tx_pda_high_unii5",
        "tx_pda_low_unii7",
        "tx_pda_mid_unii7",
        "tx_pda_high_unii7",
        "tx_ant_iso_6g",
    ],
    "6GHz Test Flow 3": [
        "tx_rf_init_cont_tx_6g_tf3",
        "tx_freq_align_6g_tf3",
        "tx_gain_6g",
    ],
    "6GHz Test Flow 4": [
        "tx_rf_init_txcal_6g",
        "tx_cal_path_6g",
        "tx_cal_iso_6g",
    ],
    "6GHz Test Flow 5": [
        "rx_rf_init_rxcal_6g_tf5",
        "rx_freq_align_6g",
        "rx_gain_nf_6g",
        "rx_ant_iso_6g",
    ],
    "6GHz Test Flow 6": [
        "rx_rf_init_rxcal_6g_tf6",
        "rx_cal_path_6g",
        "rx_cal_iso_6g",
    ],    
}

# Data-driven test specifications
# Structure: test_name -> {band, flow, sub_dir, script, args}
TEST_SPECS = {
    # ─── 3GHz Test Flow 1 ───────────────────────────────────────
    "tx_rf_init_cont_tx_3g_tf1": {
        "band": "3g",
        "flow": "tf1",
        "sub_dir": "tx_rf_init_cont_tx_3g",
        "script": "/usr/local/ntf/qa/rf/system/rf_init.ntf",
        "args_type": "rf_init_3g",
        "args_extra": "--cont-tx",
    },
    "tx_freq_align_3g_tf1": {
        "band": "3g",
        "flow": "tf1",
        "sub_dir": "tx_freq_align_3g",
        "script": "/usr/local/ntf/qa/rf/system/rn_freq_alignment.ntf",
        "args": "--freq0=3605 --freq1=3645 --txrxmode=tx",
    },
    "tx_pda_low_3g": {
        "band": "3g",
        "flow": "tf1",
        "sub_dir": "tx_pda_low_3g",
        "script": "/usr/local/ntf/qa/rf/test_qrfic_pda.ntf",
        "args_type": "pda_3g",
        "pda_variant": "low",
    },
    "tx_pda_mid_3g": {
        "band": "3g",
        "flow": "tf1",
        "sub_dir": "tx_pda_mid_3g",
        "script": "/usr/local/ntf/qa/rf/test_qrfic_pda.ntf",
        "args_type": "pda_3g",
        "pda_variant": "mid",
    },
    "tx_pda_high_3g": {
        "band": "3g",
        "flow": "tf1",
        "sub_dir": "tx_pda_high_3g",
        "script": "/usr/local/ntf/qa/rf/test_qrfic_pda.ntf",
        "args_type": "pda_3g",
        "pda_variant": "high",
    },
    "tx_ant_iso_3g": {
        "band": "3g",
        "flow": "tf1",
        "sub_dir": "tx_ant_iso_3g",
        "script": "/usr/local/ntf/qa/rf/system/tx_isolation.ntf",
        "args": "--mode=33 --freq-sweep --freq-start=3555 --freq-end=3695 --freq-step=70 --tx-atten=24 --rfdvt --set-temp={temp}",
    },
    "tx_pa_noise_3g": {
        "band": "3g",
        "flow": "tf1",
        "sub_dir": "tx_pa_noise_3g",
        "script": "/usr/local/ntf/qa/rf/system/tx_pa_noise_floor.ntf",
        "args": "--mode=33 --rfdvt --set-temp={temp} --pathloss-file {pathloss}",
    },
    "tx_vcxo_3g": {
        "band": "3g",
        "flow": "tf1",
        "sub_dir": "tx_vcxo_3g",
        "script": "/usr/local/ntf/qa/rf/system/test_vcxo_char.ntf",
        "args": "--center_freq_c0=3605 --set-temp={temp}",
    },
    # ─── 3GHz Test Flow 2 ───────────────────────────────────────
    "tx_rf_init_cont_tx_3g_tf2": {
        "band": "3g",
        "flow": "tf2",
        "sub_dir": "tx_rf_init_cont_tx_3g",
        "script": "/usr/local/ntf/qa/rf/system/rf_init.ntf",
        "args_type": "rf_init_3g",
        "args_extra": "--cont-tx",
    },
    "tx_freq_align_3g_tf2": {
        "band": "3g",
        "flow": "tf2",
        "sub_dir": "tx_freq_align_3g",
        "script": "/usr/local/ntf/qa/rf/system/rn_freq_alignment.ntf",
        "args": "--freq0=3605 --freq1=3645 --txrxmode=tx",
    },
    "tx_npr_vs_freq_sep_3g": {
        "band": "3g",
        "flow": "tf2",
        "sub_dir": "tx_npr_vs_freq_sep_3g",
        "script": "/usr/local/ntf/qa/rf/system/tx_npr_vs_freq_sep.ntf",
        "args": "--mode=33 --step-size=10 --rfdvt --set-temp={temp} --pathloss-file {pathloss}",
    },
    "tx_pd_vs_pwr_freq_3g": {
        "band": "3g",
        "flow": "tf2",
        "sub_dir": "tx_pd_vs_pwr_freq_3g",
        "script": "/usr/local/ntf/qa/rf/system/tx_pd_vs_pwr_freq.ntf",
        "args": "--mode=33 --rfdvt --set-temp={temp} --pathloss-file {pathloss}",
    },
    # ─── 3GHz Test Flow 3 ───────────────────────────────────────
    "tx_rf_init_cont_tx_3g_tf3": {
        "band": "3g",
        "flow": "tf3",
        "sub_dir": "tx_rf_init_cont_tx_3g",
        "script": "/usr/local/ntf/qa/rf/system/rf_init.ntf",
        "args_type": "rf_init_3g",
        "args_extra": "--cont-tx",
    },
    "tx_freq_align_3g_tf3": {
        "band": "3g",
        "flow": "tf3",
        "sub_dir": "tx_freq_align_3g",
        "script": "/usr/local/ntf/qa/rf/system/rn_freq_alignment.ntf",
        "args": "--freq0=3605 --freq1=3645 --txrxmode=tx",
    },
    "tx_gain_3g": {
        "band": "3g",
        "flow": "tf3",
        "sub_dir": "tx_gain_3g",
        "script": "/usr/local/ntf/qa/rf/system/tx_gain.ntf",
        "args": "--mode=33 --set-temp={temp} --pathloss-file {pathloss}",
    },
    "tx_phase_noise_3g": {
        "band": "3g",
        "flow": "tf3",
        "sub_dir": "tx_phase_noise_3g",
        "script": "/usr/local/ntf/qa/rf/system/tx_phase_noise.ntf",
        "args": "--mode=33 --set-temp={temp}",
    },
    # ─── 3GHz Test Flow 4 ───────────────────────────────────────
    "tx_rf_init_txcal_3g": {
        "band": "3g",
        "flow": "tf4",
        "sub_dir": "tx_rf_init_txcal_3g",
        "script": "/usr/local/ntf/qa/rf/system/rf_init.ntf",
        "args_type": "rf_init_3g",
        "args_extra": "--txcal",
    },
    "tx_cal_path_3g": {
        "band": "3g",
        "flow": "tf4",
        "sub_dir": "tx_cal_path_3g",
        "script": "/usr/local/ntf/qa/rf/system/txcal_path.ntf",
        "args": "--mode=33 --set-temp={temp} --TxGain-testdir {tx_gain_ref_3g}",
        "needs_ref": True,
    },
    "tx_cal_iso_3g": {
        "band": "3g",
        "flow": "tf4",
        "sub_dir": "tx_cal_iso_3g",
        "script": "/usr/local/ntf/qa/rf/system/txcal_isolation.ntf",
        "args": "--mode=33 --set-temp={temp}",
    },
    # ─── 3GHz Test Flow 5 ───────────────────────────────────────
    "rx_rf_init_rxcal_3g_tf5": {
        "band": "3g",
        "flow": "tf5",
        "sub_dir": "rx_rf_init_rxcal_3g",
        "script": "/usr/local/ntf/qa/rf/system/rf_init.ntf",
        "args_type": "rf_init_3g",
        "args_extra": "--rxcal --rxcal-rfdvt",
    },
    "rx_freq_align_3g": {
        "band": "3g",
        "flow": "tf5",
        "sub_dir": "rx_freq_align_3g",
        "script": "/usr/local/ntf/qa/rf/system/rn_freq_alignment.ntf",
        "args": "--freq0=3605 --freq1=3645 --txrxmode=rx",
    },
    "rx_gain_nf_3g": {
        "band": "3g",
        "flow": "tf5",
        "sub_dir": "rx_gain_nf_3g",
        "script": "/usr/local/ntf/qa/rf/system/rx_gain_nf.ntf",
        "args": "--mode=33 --set-temp={temp} --pathloss-file {pathloss}",
    },
    "rx_iip3_inband_3g": {
        "band": "3g",
        "flow": "tf5",
        "sub_dir": "rx_iip3_inband_3g",
        "script": "/usr/local/ntf/qa/rf/system/rx_iip3_inband.ntf",
        "args": "--mode=33 --set-temp={temp} --pathloss-file {pathloss}",
    },
    "rx_ant_iso_3g": {
        "band": "3g",
        "flow": "tf5",
        "sub_dir": "rx_ant_iso_3g",
        "script": "/usr/local/ntf/qa/rf/system/rx_antenna_isolation.ntf",
        "args": "--mode=33 --set-temp={temp} --pathloss-file {pathloss}",
    },
    "rx_iq_freq_sel_3g": {
        "band": "3g",
        "flow": "tf5",
        "sub_dir": "rx_iq_freq_sel_3g",
        "script": "/usr/local/ntf/qa/rf/system/rx_iq_freq_selectivity.ntf",
        "args": "--mode=33 --set-temp={temp} --pathloss-file {pathloss}",
    },
    # ─── 3GHz Test Flow 6 ───────────────────────────────────────
    "rx_rf_init_rxcal_3g_tf6": {
        "band": "3g",
        "flow": "tf6",
        "sub_dir": "rx_rf_init_rxcal_3g",
        "script": "/usr/local/ntf/qa/rf/system/rf_init.ntf",
        "args_type": "rf_init_3g",
        "args_extra": "--rxcal --rxcal-rfdvt",
    },
    "rx_cal_path_3g": {
        "band": "3g",
        "flow": "tf6",
        "sub_dir": "rx_cal_path_3g",
        "script": "/usr/local/ntf/qa/rf/system/rxcal_path.ntf",
        "args": "--mode=33 --set-temp={temp} --RxGain-testdir {rx_gain_ref_3g}",
        "needs_ref": True,
    },
    "rx_cal_iso_3g": {
        "band": "3g",
        "flow": "tf6",
        "sub_dir": "rx_cal_iso_3g",
        "script": "/usr/local/ntf/qa/rf/system/rxcal_isolation.ntf",
        "args": "--mode=33 --set-temp={temp}",
    },
    # ─── 6GHz Test Flow 1 ───────────────────────────────────────
    "tx_rf_init_cont_tx_6g_tf1": {
        "band": "6g",
        "flow": "tf1",
        "sub_dir": "tx_rf_init_cont_tx_6g",
        "script": "/usr/local/ntf/qa/rf/system/rf_init.ntf",
        "args_type": "rf_init_6g",
        "args_extra": "--cont-tx",
    },
    "tx_freq_align_6g_tf1": {
        "band": "6g",
        "flow": "tf1",
        "sub_dir": "tx_freq_align_6g",
        "script": "/usr/local/ntf/qa/rf/system/rn_freq_alignment.ntf",
        "args": "--freq0=6385 --freq1=6425 --txrxmode=tx",
    },
    "tx_pda_low_unii34": {
        "band": "6g",
        "flow": "tf1",
        "sub_dir": "tx_pda_low_unii34",
        "script": "/usr/local/ntf/qa/rf/test_qrfic_pda.ntf",
        "args_type": "pda_6g",
        "pda_variant": "low_unii34",
    },
    "tx_pda_mid_unii34": {
        "band": "6g",
        "flow": "tf1",
        "sub_dir": "tx_pda_mid_unii34",
        "script": "/usr/local/ntf/qa/rf/test_qrfic_pda.ntf",
        "args_type": "pda_6g",
        "pda_variant": "mid_unii34",
    },
    "tx_pda_high_unii34": {
        "band": "6g",
        "flow": "tf1",
        "sub_dir": "tx_pda_high_unii34",
        "script": "/usr/local/ntf/qa/rf/test_qrfic_pda.ntf",
        "args_type": "pda_6g",
        "pda_variant": "high_unii34",
    },
    "tx_pda_low_unii5": {
        "band": "6g",
        "flow": "tf1",
        "sub_dir": "tx_pda_low_unii5",
        "script": "/usr/local/ntf/qa/rf/test_qrfic_pda.ntf",
        "args_type": "pda_6g",
        "pda_variant": "low_unii5",
    },
    "tx_pda_mid_unii5": {
        "band": "6g",
        "flow": "tf1",
        "sub_dir": "tx_pda_mid_unii5",
        "script": "/usr/local/ntf/qa/rf/test_qrfic_pda.ntf",
        "args_type": "pda_6g",
        "pda_variant": "mid_unii5",
    },
    "tx_pda_high_unii5": {
        "band": "6g",
        "flow": "tf1",
        "sub_dir": "tx_pda_high_unii5",
        "script": "/usr/local/ntf/qa/rf/test_qrfic_pda.ntf",
        "args_type": "pda_6g",
        "pda_variant": "high_unii5",
    },
    "tx_pda_low_unii7": {
        "band": "6g",
        "flow": "tf1",
        "sub_dir": "tx_pda_low_unii7",
        "script": "/usr/local/ntf/qa/rf/test_qrfic_pda.ntf",
        "args_type": "pda_6g",
        "pda_variant": "low_unii7",
    },
    "tx_pda_mid_unii7": {
        "band": "6g",
        "flow": "tf1",
        "sub_dir": "tx_pda_mid_unii7",
        "script": "/usr/local/ntf/qa/rf/test_qrfic_pda.ntf",
        "args_type": "pda_6g",
        "pda_variant": "mid_unii7",
    },
    "tx_pda_high_unii7": {
        "band": "6g",
        "flow": "tf1",
        "sub_dir": "tx_pda_high_unii7",
        "script": "/usr/local/ntf/qa/rf/test_qrfic_pda.ntf",
        "args_type": "pda_6g",
        "pda_variant": "high_unii7",
    },
    "tx_ant_iso_6g": {
        "band": "6g",
        "flow": "tf1",
        "sub_dir": "tx_ant_iso_6g",
        "script": "/usr/local/ntf/qa/rf/system/tx_isolation.ntf",
        "args": "--mode=66 --freq-sweep --freq-start=5800 --freq-end=6800 --freq-step=500 --tx-atten=24 --rfdvt --set-temp={temp}",
    },
    "tx_pa_noise_6g": {
        "band": "6g",
        "flow": "tf1",
        "sub_dir": "tx_pa_noise_6g",
        "script": "/usr/local/ntf/qa/rf/system/tx_pa_noise_floor.ntf",
        "args": "--mode=66 --rfdvt --set-temp={temp} --pathloss-file {pathloss}",
    },
    "tx_vcxo_6g": {
        "band": "6g",
        "flow": "tf1",
        "sub_dir": "tx_vcxo_6g",
        "script": "/usr/local/ntf/qa/rf/system/test_vcxo_char.ntf",
        "args": "--center_freq_c0=6435 --set-temp={temp}",
    },
    # ─── 6GHz Test Flow 2 ───────────────────────────────────────
    "tx_rf_init_cont_tx_6g_tf2": {
        "band": "6g",
        "flow": "tf2",
        "sub_dir": "tx_rf_init_cont_tx_6g",
        "script": "/usr/local/ntf/qa/rf/system/rf_init.ntf",
        "args_type": "rf_init_6g",
        "args_extra": "--cont-tx",
    },
    "tx_freq_align_6g_tf2": {
        "band": "6g",
        "flow": "tf2",
        "sub_dir": "tx_freq_align_6g",
        "script": "/usr/local/ntf/qa/rf/system/rn_freq_alignment.ntf",
        "args": "--freq0=6385 --freq1=6425 --txrxmode=tx",
    },
    "tx_npr_vs_freq_sep_6g": {
        "band": "6g",
        "flow": "tf2",
        "sub_dir": "tx_npr_vs_freq_sep_6g",
        "script": "/usr/local/ntf/qa/rf/system/tx_npr_vs_freq_sep.ntf",
        "args": "--mode=66 --step-size=10 --rfdvt --set-temp={temp} --pathloss-file {pathloss}",
    },
    "tx_pd_vs_pwr_freq_6g": {
        "band": "6g",
        "flow": "tf2",
        "sub_dir": "tx_pd_vs_pwr_freq_6g",
        "script": "/usr/local/ntf/qa/rf/system/tx_pd_vs_pwr_freq.ntf",
        "args": "--mode=66 --rfdvt --set-temp={temp} --pathloss-file {pathloss}",
    },
    # ─── 6GHz Test Flow 3 ───────────────────────────────────────
    "tx_rf_init_cont_tx_6g_tf3": {
        "band": "6g",
        "flow": "tf3",
        "sub_dir": "tx_rf_init_cont_tx_6g",
        "script": "/usr/local/ntf/qa/rf/system/rf_init.ntf",
        "args_type": "rf_init_6g",
        "args_extra": "--cont-tx",
    },
    "tx_freq_align_6g_tf3": {
        "band": "6g",
        "flow": "tf3",
        "sub_dir": "tx_freq_align_6g",
        "script": "/usr/local/ntf/qa/rf/system/rn_freq_alignment.ntf",
        "args": "--freq0=6385 --freq1=6425 --txrxmode=tx",
    },
    "tx_gain_6g": {
        "band": "6g",
        "flow": "tf3",
        "sub_dir": "tx_gain_6g",
        "script": "/usr/local/ntf/qa/rf/system/tx_gain.ntf",
        "args": "--mode=66 --set-temp={temp} --pathloss-file {pathloss}",
    },
    "tx_phase_noise_6g": {
        "band": "6g",
        "flow": "tf3",
        "sub_dir": "tx_phase_noise_6g",
        "script": "/usr/local/ntf/qa/rf/system/tx_phase_noise.ntf",
        "args": "--mode=66 --set-temp={temp}",
    },
    # ─── 6GHz Test Flow 4 ───────────────────────────────────────
    "tx_rf_init_txcal_6g": {
        "band": "6g",
        "flow": "tf4",
        "sub_dir": "tx_rf_init_txcal_6g",
        "script": "/usr/local/ntf/qa/rf/system/rf_init.ntf",
        "args_type": "rf_init_6g",
        "args_extra": "--txcal",
    },
    "tx_cal_path_6g": {
        "band": "6g",
        "flow": "tf4",
        "sub_dir": "tx_cal_path_6g",
        "script": "/usr/local/ntf/qa/rf/system/txcal_path.ntf",
        "args": "--mode=66 --set-temp={temp} --TxGain-testdir {tx_gain_ref_6g}",
        "needs_ref": True,
    },
    "tx_cal_iso_6g": {
        "band": "6g",
        "flow": "tf4",
        "sub_dir": "tx_cal_iso_6g",
        "script": "/usr/local/ntf/qa/rf/system/txcal_isolation.ntf",
        "args": "--mode=66 --set-temp={temp}",
    },
    # ─── 6GHz Test Flow 5 ───────────────────────────────────────
    "rx_rf_init_rxcal_6g_tf5": {
        "band": "6g",
        "flow": "tf5",
        "sub_dir": "rx_rf_init_rxcal_6g",
        "script": "/usr/local/ntf/qa/rf/system/rf_init.ntf",
        "args_type": "rf_init_6g",
        "args_extra": "--rxcal --rxcal-rfdvt",
    },
    "rx_freq_align_6g": {
        "band": "6g",
        "flow": "tf5",
        "sub_dir": "rx_freq_align_6g",
        "script": "/usr/local/ntf/qa/rf/system/rn_freq_alignment.ntf",
        "args": "--freq0=6385 --freq1=6425 --txrxmode=rx",
    },
    "rx_gain_nf_6g": {
        "band": "6g",
        "flow": "tf5",
        "sub_dir": "rx_gain_nf_6g",
        "script": "/usr/local/ntf/qa/rf/system/rx_gain_nf.ntf",
        "args": "--mode=66 --set-temp={temp} --pathloss-file {pathloss}",
    },
    "rx_iip3_inband_6g": {
        "band": "6g",
        "flow": "tf5",
        "sub_dir": "rx_iip3_inband_6g",
        "script": "/usr/local/ntf/qa/rf/system/rx_iip3_inband.ntf",
        "args": "--mode=66 --set-temp={temp} --pathloss-file {pathloss}",
    },
    "rx_ant_iso_6g": {
        "band": "6g",
        "flow": "tf5",
        "sub_dir": "rx_ant_iso_6g",
        "script": "/usr/local/ntf/qa/rf/system/rx_antenna_isolation.ntf",
        "args": "--mode=66 --set-temp={temp} --pathloss-file {pathloss}",
    },
    "rx_iq_freq_sel_6g": {
        "band": "6g",
        "flow": "tf5",
        "sub_dir": "rx_iq_freq_sel_6g",
        "script": "/usr/local/ntf/qa/rf/system/rx_iq_freq_selectivity.ntf",
        "args": "--mode=66 --set-temp={temp} --pathloss-file {pathloss}",
    },
    # ─── 6GHz Test Flow 6 ───────────────────────────────────────
    "rx_rf_init_rxcal_6g_tf6": {
        "band": "6g",
        "flow": "tf6",
        "sub_dir": "rx_rf_init_rxcal_6g",
        "script": "/usr/local/ntf/qa/rf/system/rf_init.ntf",
        "args_type": "rf_init_6g",
        "args_extra": "--rxcal --rxcal-rfdvt",
    },
    "rx_cal_path_6g": {
        "band": "6g",
        "flow": "tf6",
        "sub_dir": "rx_cal_path_6g",
        "script": "/usr/local/ntf/qa/rf/system/rxcal_path.ntf",
        "args": "--mode=66 --set-temp={temp} --RxGain-testdir {rx_gain_ref_6g}",
        "needs_ref": True,
    },
    "rx_cal_iso_6g": {
        "band": "6g",
        "flow": "tf6",
        "sub_dir": "rx_cal_iso_6g",
        "script": "/usr/local/ntf/qa/rf/system/rxcal_isolation.ntf",
        "args": "--mode=66 --set-temp={temp}",
    },
}

# RF init argument templates (band-specific defaults)
RF_INIT_ARGS = {
    "3g": "--freqs=3605,3645 --cal-rx-gain=15 --cal-tx-atten=33 --data-rx-gain=48 --data-tx-atten=18 --skip-python-lo-nulling --bypass-gtest-compensations",
    "6g": "--freqs=6205,6245 --data-rx-gain=48 --data-tx-atten=18 --cal-rx-gain=9 --cal-tx-atten=27 --skip-python-lo-nulling --bypass-gtest-compensations",
}

# PDA test configurations
PDA_CONFIGS = {
    "low": {
        "fixture_loss_c0": "11.59,11.59,11.5,11.56,11.5,11.59,11.56,11.63",
        "fixture_loss_c1": "11.57,11.64,11.54,11.58,11.52,11.65,11.57,11.7",
        "carrier_freqs": "3555,3595",
        "power_levels": "36,33,30,27,24,21,18,15,12,9,6",
    },
    "mid": {
        "fixture_loss_c0": "11.56,11.62,11.53,11.6,11.51,11.62,11.57,11.7",
        "fixture_loss_c1": "11.69,11.77,11.66,11.69,11.67,11.77,11.7,11.8",
        "carrier_freqs": "3605,3645",
        "power_levels": "36,33,30,27,24,21,18,15,12,9,6",
    },
    "high": {
        "fixture_loss_c0": "11.75,11.83,11.72,11.77,11.73,11.84,11.75,11.86",
        "fixture_loss_c1": "11.7,11.74,11.67,11.68,11.66,11.77,11.7,11.77",
        "carrier_freqs": "3655,3695",
        "power_levels": "36,33,30,27,24,21,18,15,12,9,6",
    },
    "low_unii34": {
        "fixture_loss_c0": "13.46,13.46,13.44,13.54,13.36,13.42,13.33,13.43",
        "fixture_loss_c1": "13.73,13.73,13.68,13.76,13.66,13.68,13.58,13.66",
        "carrier_freqs": "5750,5790",
        "power_levels": "39,36,33,30,27,24,21,18,15,12",
    },
    "mid_unii34": {
        "fixture_loss_c0": "13.79,13.76,13.74,13.82,13.72,13.73,13.67,13.76",
        "fixture_loss_c1": "13.55,13.5,13.5,13.62,13.54,13.46,13.39,13.49",
        "carrier_freqs": "5805,5845",
        "power_levels": "39,36,33,30,27,24,21,18,15,12",
    },
    "high_unii34": {
        "fixture_loss_c0": "13.52,13.44,13.46,13.58,13.49,13.41,13.32,13.45",
        "fixture_loss_c1": "13.38,13.34,13.35,13.46,13.36,13.33,13.27,13.3",
        "carrier_freqs": "5855,5895",
        "power_levels": "39,36,33,30,27,24,21,18,15,12",
    },
    "low_unii5": {
        "fixture_loss_c0": "14.55,14.21,14.56,14.4,13.81,15.07,13.38,14.13",
        "fixture_loss_c1": "14.48,14.12,13.75,14.61,13.51,13.78,12.98,13.92",
        "carrier_freqs": "5935,5975",
        "power_levels": "39,36,33,30,27,24,21,18,15,12",
    },
    "mid_unii5": {
        "fixture_loss_c0": "13.96,13.87,13.81,13.93,13.84,13.87,13.75,13.81",
        "fixture_loss_c1": "14.01,13.84,13.84,13.98,13.88,13.9,13.79,13.88",
        "carrier_freqs": "6155,6195",
        "power_levels": "36,33,30,27,24,21,18,15,12",
    },
    "high_unii5": {
        "fixture_loss_c0": "13.99,13.99,13.86,13.93,13.77,13.93,13.91,13.89",
        "fixture_loss_c1": "14.08,14.03,13.94,13.95,13.82,13.96,13.95,13.94",
        "carrier_freqs": "6375,6415",
        "power_levels": "33,30,27,24,21,18,15,12",
    },
    "low_unii7": {
        "fixture_loss_c0": "14.18,14.14,14.03,14.02,13.9,14.04,14.1,14.05",
        "fixture_loss_c1": "14.05,14.12,13.98,13.97,13.82,13.97,14.05,13.98",
        "carrier_freqs": "6535,6575",
        "power_levels": "33,30,27,24,21,18,15,12,9",
    },
    "mid_unii7": {
        "fixture_loss_c0": "15.4,15.03,15.28,15.41,13.98,14.41,14.06,14.58",
        "fixture_loss_c1": "15.32,14.91,15.12,15.16,14.14,14.55,13.92,14.67",
        "carrier_freqs": "6680,6720",
        "power_levels": "33,30,27,24,21,18,15,12,9",
    },
    "high_unii7": {
        "fixture_loss_c0": "14.25,14.37,14.25,14.23,14.17,14.25,14.35,14.27",
        "fixture_loss_c1": "14.16,14.24,14.15,14.13,14.05,14.11,14.19,14.14",
        "carrier_freqs": "6825,6865",
        "power_levels": "33,30,27,24,21,18,15,12,9",
    },
}

# ─── Dynamic Development Enhancements ───────────────────
DEV_SLEEP_FLOW = {
    "Sleep Cmd (Dev Mode)": [
        "dev_sleep_1s",
        "dev_sleep_2s",
        "dev_sleep_3s"
    ]
} if DEV_MODE else {}

if DEV_MODE:
    # We still update TEST_SPECS so get_commands() can resolve the underlying actions
    TEST_SPECS.update({
        "dev_sleep_1s": {
            "band": "3g",
            "flow": "dev_flow",
            "sub_dir": "dev_sleep",
            "script": "sleep 1",
            "args": ""
        },
        "dev_sleep_2s": {
            "band": "3g",
            "flow": "dev_flow",
            "sub_dir": "dev_sleep",
            "script": "sleep 2",
            "args": ""
        },
        "dev_sleep_3s": {
            "band": "3g",
            "flow": "dev_flow",
            "sub_dir": "dev_sleep",
            "script": "sleep 3",
            "args": ""
        }
    })
