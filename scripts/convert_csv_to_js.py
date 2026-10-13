import argparse
import csv
import json

"""
Input values follow the definitions in readme. So expected transformations are:

- Numbers in k/M -> raw dollars
- Speed in kph -> m/s
"""

TRANSFORMS = {
    "name": lambda x: x + " (SIN)" if not str(x).endswith("(SIN)") else x,
    "age": lambda x: x * 2,
    "price": lambda x: round(x * 1.1, 2),
}

KEYS_TOP = [
    "id",
    "name",
    "description",
    "stats",
    "compatibleTrackTypes",
    "allowGradeCrossing",
    "portalCost",
    "rampCost",
    "maxOverpassSpan",
]
KEYS = {
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

FUNCTION = "window.SubwayBuilderAPI.trains.registerTrainType"


def auto_convert_val(value: str):
    if value.lower() == "true":
        return True
    elif value.lower() == "false":
        return False

    if value == "":
        return ""

    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    return value


def transform_row(row):
    result = {}

    for column, value in row.items():
        value = auto_convert_val(value)

        if column in TRANSFORMS and isinstance(value, (int, float)):
            value = TRANSFORMS[column](value)

        result[column] = value

    return result

# TODO: calc minStationLength, maxStationLength



def csv_to_js(input_file, output_file):
    with open(input_file, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        with open(output_file, "w", encoding="utf-8") as out:
            out.write("(function () {\n")

            for row in reader:
                obj = transform_row(row)

                
                js_object = json.dumps(
                    obj, ensure_ascii=False, separators=(",", ":"), allow_nan=False, indent=2
                )
                out.write(f"{FUNCTION}({js_object});\n")

            out.write("})();")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()

    csv_to_js(args.input, args.output)
