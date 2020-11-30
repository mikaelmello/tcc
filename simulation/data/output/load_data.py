import os
from os import path
from pathlib import Path
import json
import matplotlib.pyplot as plt
import pandas as pd

DIR = Path(__file__).parent.absolute()

json_files = [f for f in os.listdir(DIR) if f.endswith(".json")]
json_files.sort()
expected_delta_unit = "us"

runs = []
for filename in json_files:
    props = filename.split(".")[0]
    lang, lib, gpu, it = props.split("_")

    # if lang != "java" or lib != "deeplearning4j" or gpu != "off":
    #     continue

    print(f"loading {filename}")
    with open(path.join(DIR, filename), "r") as f:
        parsed = json.load(f)
        for idx, run in enumerate(parsed):
            if int(run["iid"]) < 3000:
                continue

            run["lang"] = lang
            run["lib"] = lib
            run["gpu"] = gpu
            run["it"] = int(it)
            run["i"] = int(run["iid"])

            if run["du"] != expected_delta_unit:
                print(f"{run} does not have expected du us")

            run.pop("du")
            run.pop("iid")
            runs.append(run)

print(f"loading dataframe")
df_all = pd.DataFrame(runs)
df = df_all.groupby(["lang", "lib", "gpu", "i"], as_index=False).median()
