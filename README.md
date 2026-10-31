# Datasheet Collection

This folder contains component datasheets, module specifications, package references, and marking guides. It currently holds 33 PDF files. Filenames usually identify the main part or document; consult each manufacturer's datasheet for exact ratings, ordering codes, package drawings, and revision information.

## IGBT modules and power modules

| File | What it covers |
|---|---|
| `6MBI100S-120.pdf` | Fuji Electric 6-in-1 IGBT module, 1200 V / 100 A, for motor drives, servo amplifiers, UPS equipment, and industrial machines. |
| `PM200CLA120.pdf` | Mitsubishi intelligent power module (IPM), model PM200CLA120. |
| `SEMIKRON_SKiiP_39AC12T4V1_25231450.pdf` | Semikron SKiiP 39AC12T4V1 six-pack IGBT module datasheet. |
| `SKiiP31NAB12T11.pdf` | Semikron SKiiP31NAB12T11 IGBT power module datasheet; 1200 V class. |
| `SKM150GB123D.PDF` | Semikron SKM150GB123D SEMITRANS 3 dual IGBT half-bridge module datasheet (1200 V, 150 A). |
| `SKM150GB123D_related_reference_only.pdf` | Two-page distributor product listing for a used SKM150GB123D module. This is not the manufacturer's datasheet and should not be used as a substitute for it. |
| `v23990-k219F4004.pdf` | Vincotech MiniSKiiP 1-pack IGBT module, model V23990-K219-F-PM; 1200 V / 15 A. |
| `Vincotech_V23990-K210-F40_FD-Rev_04.pdf` | Vincotech MiniSKiiP 1-pack IGBT module datasheet, model V23990-K210-F40-PM; 1200 V / 25 A, revision 4. |

## Gate drivers, optocouplers, and isolation

| File | What it covers |
|---|---|
| `ACPL-332J_Datasheet.pdf` | Broadcom ACPL-332J intelligent gate-drive optocoupler, with IGBT fault detection and protection features. |
| `ACPL-333J_Datasheet.pdf` | Broadcom ACPL-333J intelligent gate-drive optocoupler, including auto-fault reset. |
| `FOD3150A_Datasheet.pdf` | onsemi FOD3150A 2.5 A gate-drive optocoupler for IGBTs and MOSFETs. |
| `HCPL-7800.pdf` | HCPL-7800 family isolation amplifier datasheet for isolated analog signal measurement. |

## Relays and relay interfaces

| File | What it covers |
|---|---|
| `AQ2A2-C1-T5VDC_Datasheet.pdf` | Panasonic/NAIS AQ8 solid-state relay product catalog, including the AQ2A2-C1-T5VDC family. |
| `HFA2 Relay.pdf` | Hongfa HFA2 safety relay with forcibly guided contacts; includes contact arrangements, electrical limits, and coil data. |
| `NAIS_AC4-15-L_IO_Relay_Datasheet.pdf` | Panasonic/NAIS AC4/15-L input/output relay modules for interfacing a controller or CPU with external inputs and loads. |

## Discrete semiconductors and power supply parts

| File | What it covers |
|---|---|
| `BSP 452.pdf` | Infineon BSP452 MiniPROFET high-side switch with overload, short-circuit, thermal, and inductive-load protection. |
| `FQPF6N60C.pdf` | Fairchild/onsemi FQPF6N60C 600 V N-channel MOSFET in an insulated TO-220F package. |
| `lm2576.pdf` | Texas Instruments LM2576 3 A step-down switching voltage regulator family. |
| `LM386 Datasheet.pdf` | UTC LM386 low-voltage audio power amplifier. |
| `SC92F7421M_Datasheet.pdf` | SinOne SC92F7423/7422/7421/7420 8051-based Flash microcontroller family; includes the SC92F7421M part. |
| `SN65HVD230_Datasheet.pdf` | Texas Instruments SN65HVD230/231/232 3.3 V CAN bus transceiver family. |
| `STP6NK60ZFP.pdf` | STMicroelectronics 600 V N-channel SuperMESH power MOSFET family, including the STP6NK60ZFP. |
| `VIPER27L_Datasheet.pdf` | STMicroelectronics VIPER27 offline high-voltage converter; the L version operates at 60 kHz. |
| `VS010-0505SE.pdf` | VS010 isolated DC-DC converter family, including 5 V input / 5 V single-output variants. |

## TVS and Zener diodes

| File | What it covers |
|---|---|
| `PJ_DO-214AC_P4SMA110CA_Fagor_TVS_Datasheet.pdf` | Fagor P4SMA surface-mount TVS diode family in DO-214AC (SMA), covering multiple voltage ratings. `P4SMA110CA` in the filename is a candidate identification; confirm the device's full marking and electrical requirements before selecting a replacement. |
| `LT_SOD323_Nexperia_PZU6.8B2A_Datasheet.pdf` | Nexperia PZUxBA Zener diode family in SOD323 (SC-76), including the PZU6.8B2A range. |
| `PZUXBA_SER-1319361.pdf` | Another copy of the Nexperia PZUxBA SOD323 Zener family datasheet. It is byte-for-byte identical to `LT_SOD323_Nexperia_PZU6.8B2A_Datasheet.pdf`. |
| `SMBJ18A_LT_DO-214AA_Datasheet.pdf` | Alpha & Omega Semiconductor SMBJ TVS diode family in DO-214AA (SMB), 600 W class, with uni- and bidirectional variants. |
| `SMBJ18A_LT_DO-214AA_Marking.pdf` | AOS SMBJ package marking note. It maps `LT` to the SMBJ18A part code and explains the year/week date codes. |
| `smbj5.0a-smbj170a_diodes.pdf` | Diodes Incorporated SMBJ5.0(C)A through SMBJ170(C)A 600 W TVS diode family. |

## Package and component references

| File | What it covers |
|---|---|
| `SMD Dimension Selection Guide.pdf` | MCC Semiconductor package-outline and package-name cross-reference guide. Use it to compare package families; verify dimensions against the component manufacturer's drawing. |
| `SMD_Package_Size_Reference_Guide.pdf` | First edition of the local SMD package size reference guide. |
| `SMD_Package_Size_Reference_Guide_v2.pdf` | Updated local SMD package size reference guide with expanded cross-check notes and package dimensions. |

## Notes

- There are 33 PDFs in the collection. Some are full product-family datasheets, not specifications for only one orderable part.
- Part-number markings can be ambiguous. Package size, circuit role, manufacturer, and electrical measurements may be needed to identify a component reliably.
- `SKM150GB123D.PDF` is the technical datasheet copy; the similarly named `SKM150GB123D_related_reference_only.pdf` is a distributor listing.
- The two PZUxBA PDFs are identical copies. Both names are retained to preserve the existing file collection.

## Other files

- `smd_package_guide.py` is a helper script associated with the SMD package reference materials.
- `smd-components-and-their-package-size.jpg` is a visual package-size reference image.
