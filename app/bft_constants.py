"""BFT test definitions and command specifications."""

BFT_TESTS = [
    "cal_set_freq_test",
    "rf_init_g2_rn_3ghz",
    "mfg_pda_g2_rn_3ghz",
    "rf_init_g2_rn_6ghz",
    "mfg_pda_g2_rn_6ghz",
]

PDA_CONFIGS = {
    "3ghz": {
        "fixture_loss_c0": "8.09,8.43,8.80,8.57,8.53,8.14,8.11,8.02",
        "fixture_loss_c1": "8.17,8.58,8.11,8.61,8.72,8.28,8.22,8.14",
    },
    "6ghz": {
        "fixture_loss_c0": "11.8,11.75,11.78,11.34,11.69,11.32,11.48,11.58",
        "fixture_loss_c1": "10.77,11.03,11.21,10.73,10.76,10.9,11.11,11.15",
    },
}

BFT_SPECS = {
    "cal_set_freq_test": {
        "sub_dir": "cal_set_freq_test",
        "script": "/usr/local/ntf/system/cal_set_freq_test.ntf",
        "args": "",
    },
    "rf_init_g2_rn_3ghz": {
        "sub_dir": "rf_init_g2_rn_3ghz",
        "script": "/usr/local/ntf/qa/rf/system/mfg_ntfs/rf_init_g2_rn_3ghz.ntf",
        "args": "",
    },
    "mfg_pda_g2_rn_3ghz": {
        "sub_dir": "mfg_pda_g2_rn_3ghz",
        "script": "/usr/local/ntf/qa/rf/pda/mfg_pda_g2_rn_3ghz.ntf",
        "args_type": "pda",
        "band": "3ghz",
    },
    "rf_init_g2_rn_6ghz": {
        "sub_dir": "rf_init_g2_rn_6ghz",
        "script": "/usr/local/ntf/qa/rf/system/mfg_ntfs/rf_init_g2_rn_6ghz.ntf",
        "args": "",
    },
    "mfg_pda_g2_rn_6ghz": {
        "sub_dir": "mfg_pda_g2_rn_6ghz",
        "script": "/usr/local/ntf/qa/rf/pda/mfg_pda_g2_rn_6ghz.ntf",
        "args_type": "pda",
        "band": "6ghz",
    },
}
