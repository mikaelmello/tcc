import os
from os import path
from pathlib import Path
import json
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

matplotlib.use("TKagg")

plt.rc("text", usetex=True)
# font = {'family':'serif','size':16}
font = {"family": "sans-serif", "size": 18, "serif": ["computer modern roman"]}
plt.rc("font", **font)
plt.rc("legend", **{"fontsize": 16})
matplotlib.rcParams["text.latex.preamble"] = [r"\usepackage{amsmath}"]


def get_runtime(key):
    return {
        "onnx": "ONNX Runtime",
        "tensorflow": "TensorFlow",
        "tensorflowlite": "TensorFlow Lite",
        "opencv": "OpenCV",
        "deeplearning4j": "Deeplearning4j",
    }[key]


def get_language(key):
    return {"java": "Java", "python": "Python"}[key]


def get_gpu_status(key):
    return {
        "off": "sem GPU",
        "on": "com GPU",
    }[key]


def get_label(key):
    print(key)
    return f"{get_language(key[0])}, {get_runtime(key[1])}, {get_gpu_status(key[2])}"


def plot_lines(df, queries=[], groupby=["lang", "lib", "gpu"], kind="line"):
    fig, ax = plt.subplots()

    for i in queries:
        df = df.query(i)

    for key, grp in df.groupby(groupby):
        if key == (None, None, None):
            print(key, grp)

        ax = grp.plot(ax=ax, kind=kind, x="i", y="d", label=get_label(key))

    ticks = []
    for i in range(3000, 97301, 6000):
        ticks.append(i)
    plt.xticks(ticks)
    plt.xlabel("Execução")
    plt.ylabel("Tempo de execução (µs)")
    plt.show()


def plot_box(df, queries=[], groupby=["lang", "lib", "gpu"]):
    fig, ax = plt.subplots()

    for i in queries:
        df = df.query(i)

    for key, grp in df.groupby(groupby):
        if key == (None, None, None):
            print(key, grp)

        ax = grp.boxplot(ax=ax, by="d")

    plt.show()