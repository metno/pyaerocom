# Variable names for which mda8 values are to be calculated.
MDA8_INPUT_VARS = ("conco3", "vmro3")
MDA8_OUTPUT_VARS = (
    "conco3mda8",
    "vmro3mda8",
)
# somo currently only working with vmro3 since threshold is defined in ppb
SOMO30_INPUT_VARS = ("vmro3",)  # ("conco3", "vmro3")
SOMO30_OUTPUT_VARS = (
    # "conco3somo30",
    "vmro3somo30",
)
