#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =========================
# CONFIGURACIÓN DE INPUT
# =========================

box = "Box05_checked/Tray000144_checked"
base_path = f"input/{box}"

# =========================
# CONTENIDO GENERAL
# =========================

contents = {
    "Sources": [],
    "Encoders": [],
    "Values": {},
}

contents["Values"].update(
    {
        "Part Type ID": "Z00100300029",
        "Part Type Name": "Z.Sandbox.HWDBUnitTest.fribble",
    }
)

# =========================
# SOURCES
# =========================

src_item = {
    "Source Name": "Item Source",
    "Files": f"{base_path}/SiPM-item-manifest.xlsx",
    "Encoder": "Item Encoder",
    "Values": {
        "Enabled": True,
    }
}

src_dnsc = {
    "Source Name": "Dark Noise SiPM Counts",
    "Files": f"{base_path}/Dark-noise-SiPM-counts.xlsx",
    "Encoder": "Dark Noise SiPM Counts Encoder",
}

src_char = {
    "Source Name": "IV SiPM Characterization",
    "Files": f"{base_path}/IV-SiPM-characterization.xlsx",
    "Encoder": "IV SiPM Characterization Encoder",
}

src_noise = {
    "Source Name": "IV SiPM Noise Test",
    "Files": f"{base_path}/IV-SiPM-noise-test.xlsx",
    "Encoder": "IV SiPM Noise Test Encoder",
}

src_mass = {
    "Source Name": "SiPM Mass Test",
    "Files": f"{base_path}/SiPM-mass-test-results.xlsx",
    "Encoder": "SiPM Mass Test Encoder",
}

contents["Sources"].extend([
    src_item,
    src_dnsc,
    src_char,
    src_noise,
    src_mass
])

# =========================
# ENCODERS
# =========================

enc_item = {
    "Encoder Name": "Item Encoder",
    "Record Type": "Item",
    "Part Type Name": "Z.Sandbox.HWDBUnitTest.fribble",
    "Part Type ID": "Z00100300029",
    "Schema": {
        "Manufacturer Name": {
            "column": "Manufacturer",
        },
        "Manufacturer": {
            "value": None,
        },
        "Specifications": {
            "SiPM_Strip_ID": "string",
            "Vendor": "string",
            "Vendor_Delivery_ID": "string",
            "Vendor_Box_Number": "integer",
            "Tray_Number": "integer",
            "Test_Box_ID": "string",
            "Documentation": "string",
        }
    }
}

enc_dnsc = {
    "Encoder Name": "Dark Noise SiPM Counts Encoder",
    "Record Type": "Test",
    "Part Type Name": "Z.Sandbox.HWDBUnitTest.wibble",
    "Part Type ID": "Z00100300025",
    "Test Name": "Dark Noise SiPM Counts",
    "Schema": {
        "Serial Number": {
            "type": "null,string",
            "column": "SiPM_Strip_ID",
        },
        "Test Results": {
            "DATA": {
                "type": "group",
                "key": ["Date", "Location"],
                "members": {
                    "Date": "string",
                    "Location": "string",
                    "Operator": "string",
                    "Thermal_Cycle": "integer",
                    "Polarization": "string",
                    "Temperature": "string",
                    "Acquisition_Time": "integer",
                    "Weighted_Threshold_Charge": "integer",
                    "SiPM": {
                        "type": "group",
                        "key": "SiPM_Location",
                        "members": {
                            "SiPM_Location": "integer",
                            "OV": "float",
                            "Counts": "integer",
                            "Status": "string",
                            "Comment": "string",
                        }
                    }
                }
            }
        }
    }
}

enc_char = {
    "Encoder Name": "IV SiPM Characterization Encoder",
    "Record Type": "Test",
    "Part Type Name": "Z.Sandbox.HWDBUnitTest.wibble",
    "Part Type ID": "Z00100300025",
    "Test Name": "IV SiPM Characterization",
    "Schema": {
        "Serial Number": {
            "type": "null,string",
            "column": "SiPM_Strip_ID",
        },
        "Test Results": {
            "DATA": {
                "type": "group",
                "key": ["Date", "Location", "Polarization"],
                "members": {
                    "Date": "string",
                    "Location": "string",
                    "Operator": "string",
                    "Thermal_Cycle": "integer",
                    "Polarization": "string",
                    "Temperature": "string",
                    "R_cable": "float",
                    "R_eff": "float",
                    "SiPM": {
                        "type": "group",
                        "key": "SiPM_Location",
                        "members": {
                            "SiPM_Location": "integer",
                            "V": "array",
                            "I": "array",
                            "I_Err": "array",
                            "Fit_range_low": "float,null",
                            "Fit_Polynomial_Degree": "integer,null",
                            "Status": "string",
                            "Comment": "string",
                        }
                    }
                }
            }
        }
    }
}

enc_noise = {
    "Encoder Name": "IV SiPM Noise Test Encoder",
    "Record Type": "Test",
    "Part Type Name": "Z.Sandbox.HWDBUnitTest.wibble",
    "Part Type ID": "Z00100300025",
    "Test Name": "IV SiPM Noise Test",
    "Schema": {
        "Serial Number": {
            "type": "null,string",
            "column": "SiPM_Strip_ID",
        },
        "Test Results": {
            "DATA": {
                "type": "group",
                "key": ["Date", "Location"],
                "members": {
                    "Date": "string",
                    "Location": "string",
                    "Operator": "string",
                    "Thermal_Cycle": "integer",
                    "Polarization": "string",
                    "Temperature": "string",
                    "SiPM": {
                        "type": "group",
                        "key": "SiPM_Location",
                        "members": {
                            "SiPM_Location": "integer",
                            "V": "array",
                            "I": "array",
                            "V_Range_Low": "array",
                            "I_Mean_Low": "float",
                            "V_Range_High": "array",
                            "I_Mean_High": "float",
                            "I_Rel_Diff": "float",
                            "Status": "string",
                            "Comment": "string",
                        }
                    }
                }
            }
        }
    }
}

enc_mass = {
    "Encoder Name": "SiPM Mass Test Encoder",
    "Record Type": "Test",
    "Part Type Name": "Z.Sandbox.HWDBUnitTest.wibble",
    "Part Type ID": "Z00100300025",
    "Test Name": "SiPM Mass Test",
    "Schema": {
        "Serial Number": {
            "type": "null,string",
            "column": "SiPM_Strip_ID",
        },
        "Test Results": {
            "DATA": {
                "type": "group",
                "key": ["Date", "Location", "Measured_Attribute"],
                "members": {
                    "Date": "string",
                    "Location": "string",
                    "Operator": "string",
                    "Thermal_Cycle": "integer",
                    "Polarization": "string",
                    "Temperature": "string",
                    "Manufacturer": "string",
                    "Measured_Attribute": "string",
                    "SiPM": {
                        "type": "group",
                        "key": "SiPM_Location",
                        "members": {
                            "SiPM_Location": "integer",
                            "Result": "float",
                            "Result_Err": "float,null",
                            "Strip_Avg_Result": "float",
                        }
                    }
                }
            }
        }
    }
}

contents["Encoders"].extend([
    enc_item,
    enc_dnsc,
    enc_char,
    enc_noise,
    enc_mass
])

# =========================
# DEBUG OUTPUT
# =========================

if __name__ == "__main__":
    import json
    print(json.dumps(contents, indent=4))