import time
import os
import argparse
import json
from classifier import Classifier
from zipfile import ZipFile


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", "-m", required=True, type=str)
    parser.add_argument("--input-path", "-i", required=True, type=str)
    parser.add_argument("--output-path", "-o", required=True, type=str)
    parser.add_argument("--gpu", "-g", action="store_true", default=False)

    args = vars(parser.parse_args())
    return args


class Input:
    def __init__(self, input_path):
        self.input_zip = ZipFile(input_path)
        self.to_open = self.input_zip.namelist()
        self.open = False

    def get_next(self):
        while True:
            if not self.open:
                if not self.to_open:
                    return

                filename = self.to_open[0]
                self.to_open = self.to_open[1:]
                content = self.input_zip.read(filename)
                self.cur_file = json.loads(content.decode("utf8"))
                self.open = True
                self.cur_index = 0

            inputs = self.cur_file["inputs"]
            count = self.cur_file["count"]
            payload = inputs[self.cur_index]

            self.cur_index += 1
            if self.cur_index == count:
                self.open = False

            yield payload


class Output:
    def __init__(self, output_path):
        self.output_path = output_path
        self.results = []

    def register_result(self, td, output, inp):
        output_payload = {
            "iid": inp["id"],
            "o": output,
            "eo": inp["expected_output"],
            "d": td,
            "du": "us",
        }

        self.results.append(output_payload)

    def save(self):
        with open(self.output_path, "w") as f:
            json.dump(self.results, f, separators=(",", ":"))


def classify(classifier, data):
    start = time.time()
    res = classifier.classify(data)
    end = time.time()

    microseconds = int((end - start) * 1e6)
    return (res, microseconds)


if __name__ == "__main__":
    args = parse_args()

    model_path = os.path.join(args["model_path"], "model.h5")
    input_path = args["input_path"]
    output_path = args["output_path"]

    classifier = Classifier(model_path)
    data = Input(input_path)
    output = Output(output_path)

    count = 0
    for inp in data.get_next():
        if count % 1000 == 0:
            print(f"\r{count} registered...", end="")
        result = classify(classifier, inp["data"])
        output.register_result(result[1], result[0], inp)
        count += 1

    print("\nSaving!")
    output.save()
    print("Done!")
