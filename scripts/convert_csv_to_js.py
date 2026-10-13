import argparse
import csv
import json
import math

"""
Input values follow the definitions in readme. So expected transformations are:

- Numbers in k/M -> raw dollars
- Speed in kph -> m/s
"""

# TRANSFORMS = {
#     "name": lambda x: x + " (SIN)" if not str(x).endswith("(SIN)") else x,
#     "age": lambda x: x * 2,
#     "price": lambda x: round(x * 1.1, 2),
# }


def process_track_types(row: dict):
    if not row["compatibleTrackTypes"]:
        return [row["id"]]

    if isinstance(row["compatibleTrackTypes"], str):
        return [row["id"], row["compatibleTrackTypes"]]

    return [row["id"]] + row["compatibleTrackTypes"]

# also includes modifications lol
ADDITIONAL_VALUES = {
    "name": lambda row: row["name"] + " (SIN)",
    "minStationLength": lambda row: int(
        math.ceil(int(row["minCars"]) * float(row["carLength"]))
    ),
    "maxStationLength": lambda row: int(
        math.ceil(int(row["maxCars"]) * float(row["carLength"]))
    ),
    "compatibleTrackTypes": process_track_types,
}

SUFFIX_UNIT_COEFFS = {"_kph": 1 / 3.6, "_M": 1e6, "_k": 1e3}

KEYS_L1 = [
    "id",
    "name",
    "description",
    "stats",
    "compatibleTrackTypes",
    "appearance",
    "allowGradeCrossing",
    "portalCost",
    "rampCost",
    "maxOverpassSpan",
]
KEYS_L2 = {
    "stats": [
        "maxSpeed",
        "maxAcceleration",
        "maxDeceleration",
        "maxLateralAcceleration",
        "maxCantMm",
        "maxCantDeficiencyMm",
        "maxSlopePercentage",
        "maxSpeedLocalStation",
        "crossoverSpeed",
        "yardSpeedLimit",
        "stopTimeSeconds",
        "turnaroundTimeSeconds",
        "minTurnRadius",
        "minStationTurnRadius",
        "parallelTrackSpacing",
        "trackClearance",
        "minCars",
        "maxCars",
        "carsPerCarSet",
        "capacityPerCar",
        "seatsPerCar",
        "doorsPerCarPerSide",
        "carLength",
        "trainWidth",
        "carCost",
        "minStationLength",
        "maxStationLength",
        "baseTrackCost",
        "baseStationCost",
        "scissorsCrossoverCost",
        "trainOperationalCostPerHour",
        "carOperationalCostPerHour",
        "trackMaintenanceCostPerMeter",
        "stationMaintenanceCostPerYear",
        "tphLimit",
    ],
    "appearance": ["color", "roofStyle", "couplerWidthMultiplier", "catenary"],
}

FN_NAME = "window.SubwayBuilderAPI.trains.registerTrainType"

ALLOWED_MISSING_KEYS = {"stats.minStationLength", "stats.maxStationLength"}


def auto_convert_str_to_type(value: str):
    if value.lower() == "true":
        return True
    elif value.lower() == "false":
        return False

    if value == "":
        return ""

    if "," in value:
        return list(value.split(","))

    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    return value.strip()


def check_all_keys(row: dict) -> bool:
    keys_not_found = set()

    row_keys_without_suffix = [k.split("_")[0] for k in row.keys()]
    for k1 in KEYS_L1:
        if k1 in KEYS_L2:
            continue

        if k1 not in row_keys_without_suffix:
            keys_not_found.add(k1)

    for k1, k2s in KEYS_L2.items():
        for k2 in k2s:
            if k2 not in row_keys_without_suffix:
                keys_not_found.add(f"{k1}.{k2}")

    for allowed in ALLOWED_MISSING_KEYS:
        if allowed in keys_not_found:
            keys_not_found.remove(allowed)

    if keys_not_found:
        print("Unexpected missing keys in csv:")
        print("\n".join(keys_not_found))
        return False

    return True


def process_key_value(key: str, value):
    """
    Handles unit conversions specified by key suffix.
    """

    if "_" not in key:
        return key, value

    for suffix, coeff in SUFFIX_UNIT_COEFFS.items():
        if key.endswith(suffix):
            return key.split("_")[0], value * coeff

    print(f"Warning: unrecognized suffix for csv key: {key}")
    return key, value


def transform_row(row: dict):
    out = {key: {} for key in KEYS_L1}

    keylist_l1 = [k for k in KEYS_L1 if k not in KEYS_L2]

    for key, value in row.items():
        value = auto_convert_str_to_type(value)
        row[key] = value  # save back, need later

        key, value = process_key_value(key, value)

        if key in keylist_l1:
            out[key] = value
            continue

        for k1, k2s in KEYS_L2.items():
            if key in k2s:
                out[k1][key] = value
                continue

    # now add extra keys
    for key, fn in ADDITIONAL_VALUES.items():
        value = fn(row)

        if key in keylist_l1:
            out[key] = value
            continue

        for k1, k2s in KEYS_L2.items():
            if key in k2s:
                out[k1][key] = value
                continue

    return out


# TODO: calc minStationLength, maxStationLength


def main(input_file: str, output_file: str):
    with open(input_file, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        with open(output_file, "w", encoding="utf-8") as out:
            out.write("(function () {\n")

            keys_checked = False

            for row in reader:
                if not keys_checked:
                    if not check_all_keys(row):
                        input("Proceed with missing keys?")
                    keys_checked = True
                    print("CSV key check passed.")

                obj = transform_row(row)

                js_object = json.dumps(
                    obj,
                    ensure_ascii=False,
                    separators=(",", ":"),
                    allow_nan=False,
                    indent=2,
                )
                out.write(f"{FN_NAME}({js_object});\n")

            out.write("})();")

    print("Conversion complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()

    main(args.input, args.output)
