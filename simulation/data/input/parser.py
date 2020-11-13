import random
import numpy as np
import pandas as pd
import re
import uuid
import json
import hashlib
import io
from zipfile import ZipFile, ZIP_DEFLATED
from concurrent.futures import as_completed, ProcessPoolExecutor, wait

from os import listdir

file_regex = r"(\d+)_([A-Za-z_\d]+)_(\d*)_state_(\d+)\.txt"


def progressBar(iterable):
    total = len(iterable)
    largest = 0

    # Progress Bar Printing Function
    def printProgressBar(iteration, suf):
        percent = ("{0:.2f}").format(100 * (iteration / float(total)))

        filledLength = int(20 * iteration // total)
        bar = "█" * filledLength + "_" * (20 - filledLength)

        content = f"\rProgress |{bar}| {percent}% {suf}"
        lg = max(largest, len(content))
        missing = lg - len(content)
        content += " " * missing

        print(content, end="")

        return lg

    # Initial Call
    printProgressBar(0, "")
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        largest = max(largest, printProgressBar(i + 1, item))
    # Print New Line on Complete
    print()


file_id = 0


def parse_file(file, content):
    global file_id
    matches = re.findall(file_regex, file)
    seed, alg, load, it = matches[0]

    tlc = 86
    tfc = 86 * 320

    data = pd.read_csv(io.BytesIO(content), delimiter=";")
    data = data.drop(["Unnamed: 320"], axis=1)

    data = data[0:tlc].values
    data = data.reshape(1, -1)

    actual_data = [[]]
    for i in range(0, tfc, 1):
        if data[0][i] != 0:
            data[0][i] = 1
        actual_data[0].append(int(data[0][i]))

    expected_output = {
        "MAdapSPV": 2,
        "K5SP_CS": 2,
        "K2SP_LastFit": 1,
        "K5SP_Random": 0,
    }

    payload = {
        "id": file_id,
        "seed": seed,
        "alg": alg,
        "load": load,
        "it": it,
        "data": actual_data,
        "expected_output": expected_output.setdefault(alg, 3),
    }
    file_id += 1

    return payload


input_zip = ZipFile("dataset.zip")
output_zip = ZipFile("workload.zip", "w", ZIP_DEFLATED)

batch = 500
cur = []
cur_i = 0

workload_id = 0


def process():
    global cur_i
    global cur
    global output_zip
    global workload_id

    if not cur:
        return
    workload = {
        "id": workload_id,
        "count": len(cur),
        "inputs": cur,
    }

    workload_id += 1

    content = json.dumps(workload, separators=(",", ":"))
    output_zip.writestr(f"{cur_i}.json", content)
    cur = []
    cur_i += 1


namelist = input_zip.namelist()
random.shuffle(namelist)

for filename in progressBar(namelist):
    content = input_zip.read(filename)
    parsed = parse_file(filename, content)

    cur.append(parsed)
    if len(cur) >= batch:
        process()

process()
output_zip.close()


# files = []
# batch = 500
# for i in range(0, len(filenames), batch):
#     files.append(filenames[i : i + batch])

# for i in range(len(files)):
#     print(f"{i} starting...")
#     workload = {
#         "id": uuid.uuid4().hex,
#         "count": 0,
#         "inputs": [],
#     }

#     with ProcessPoolExecutor(max_workers=7) as e:
#         futuresLst = [e.submit(parse_file, f) for f in files[i]]
#         for future in as_completed(futuresLst):
#             try:
#                 workload["inputs"].append(future.result())
#             except Exception as exc:
#                 print("%r generated an exception: %s" % (future, exc))

#         wait(futuresLst)
#         e.shutdown(True)

#     with open(f"workload/{i}.json", "w") as json_file:
#         json.dump(workload, json_file, separators=(",", ":"))

#     print(f"{i} ended")
