#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =========================
# CONFIGURACIÓN DE INPUT
# =========================

box = "Box33_checked/Tray000086_checked"
base_path = f"input/{box}"

# =========================
# CONTENIDO GENERAL
# =========================

contents = \
{
    "Sources": [],
    "Encoders": [],
    "Values": {},
}

# Append some global values
# Values can also be set at the Source or Sheet level, but they must not
# conflict with a value set higher up the chain. If a value needs to be
# different things in different places, set them at the level that they
# are needed, not at the global level.
# This was a design choice we made to reduce the chances of causing hidden
# problems that are hard for the end-user to track down. It would be easier
# to just allow overriding, so if this feature proves unpopular, we could
# change it.
contents["Values"].update(
    {
        "Part Type ID": "D00400100003",
        "Part Type Name": "D.FD-HD PDS.Module.SiPM board",
    })

# Append some sources
src_item = {
        "Source Name": "Item Source",
        "Files": f"{base_path}/SiPM-item-manifest.xlsx",
        "Encoder": "Item Encoder",
        "Values":
        {
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
        "Source Name": "SiPM Mass Test Results",
        "Files": f"{base_path}/SiPM-mass-test-results.xlsx",
        "Encoder": "SiPM Mass Test Results Encoder",
    }

contents["Sources"].append(src_item)
contents["Sources"].append(src_dnsc)
contents["Sources"].append(src_char)
contents["Sources"].append(src_noise)
contents["Sources"].append(src_mass)

# Append some encoders
enc_item = {
        "Encoder Name": "Item Encoder",
        "Record Type": "Item",
        "Part Type Name": "D.FD-HD PDS.Module.SiPM board",
        "Part Type ID": "D00400100003",
        "Schema":
        {
            "Manufacturer Name":
            {
                "column": "Manufacturer",  
            },
            "Manufacturer":
            {
                "value": None,
            },
            "Specifications":
            {
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
        "Part Type Name": "D.FD-HD PDS.Module.SiPM board",
        "Part Type ID": "D00400100003",
        "Test Name": "Dark Noise SiPM Counts",
        "Schema":
        {
            "Serial Number":
            {
                "type": "null,string",
                "column": "SiPM_Strip_ID",
            },
            "Test Results":
            {
                "Test Results":
                {
                    "type": "group",
                    "key": ["Date", "Location"],
                    "members":
                    {
                        "Date": "string",
                        "Location": "string",
                        "Operator": "string",
                        "Thermal_Cycle": "integer",
                        "Polarization": "string",
                        "Temperature": "string",
                        "Acquisition_Time": "integer",
                        "Weighted_Threshold_Charge": "integer",
                        "SiPM":
                        {
                            "type": "group",
                            "key": "SiPM_Location",
                            "members":
                            {
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
        "Part Type Name": "D.FD-HD PDS.Module.SiPM board",
        "Part Type ID": "D00400100003",
        "Test Name": "IV SiPM Characterization",
        "Schema":
        {
            "Serial Number":
            {
                "type": "null,string",
                "column": "SiPM_Strip_ID",
            },
            "Test Results":
            {
                "Test Results":
                {
                    "type": "group",
                    "key": ["Date", "Location","Polarization"],
                    "members":
                    {
                        "Date": "string",
                        "Location": "string",
                        "Operator": "string",
                        "Thermal_Cycle": "integer",
                        "Polarization": "string",
                        "Temperature": "string",
                        "R_cable": "float",
                        "R_eff": "float",
                        "SiPM":
                        {
                            "type": "group",
                            "key": "SiPM_Location",
                            "members":
                            {
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
        "Part Type Name": "D.FD-HD PDS.Module.SiPM board",
        "Part Type ID": "D00400100003",
        "Test Name": "IV SiPM Noise Test",
        "Schema":
        {
            "Serial Number":
            {
                "type": "null,string",
                "column": "SiPM_Strip_ID",
            },
            "Test Results":
            {
                "Test Results":
                {
                    "type": "group",
                    "key": ["Date", "Location"],
                    "members":
                    {
                        "Date": "string",
                        "Location": "string",
                        "Operator": "string",
                        "Thermal_Cycle": "integer",
                        "Polarization": "string",
                        "Temperature": "string",
                        "SiPM":
                        {
                            "type": "group",
                            "key": "SiPM_Location",
                            "members":
                            {
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
        "Encoder Name": "SiPM Mass Test Results Encoder",
        "Record Type": "Test",
        "Part Type Name": "D.FD-HD PDS.Module.SiPM board",
        "Part Type ID": "D00400100003",
        "Test Name": "SiPM Mass Test Results",
        "Schema":
        {
            "Serial Number":
            {
                "type": "null,string",
                "column": "SiPM_Strip_ID",
            },
            "Test Results":
            {
                "Test Results":
                {
                    "type": "group",
                    "key": ["Date", "Location","Measured_Attribute"],
                    "members":
                    {
                        "Date": "string",
                        "Location": "string",
                        "Operator": "string",
                        "Thermal_Cycle": "integer",
                        "Polarization": "string",
                        "Temperature": "string",
                        "Manufacturer": "string",
                        "Measured_Attribute": "string",
                        "SiPM":
                        {
                            "type": "group",
                            "key": "SiPM_Location",
                            "members":
                            {
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

contents["Encoders"].append(enc_item)
contents["Encoders"].append(enc_dnsc)
contents["Encoders"].append(enc_char)
contents["Encoders"].append(enc_noise)
contents["Encoders"].append(enc_mass)


# The following code is not necessary. It merely displays the resulting JSON
# version of the docket, if this script is run directly. It may be useful for
# troubleshooting.
if __name__ == '__main__':
    import json
    print(json.dumps(contents, indent=4))



























