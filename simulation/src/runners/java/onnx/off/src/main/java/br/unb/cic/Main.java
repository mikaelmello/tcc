package br.unb.cic;

import com.google.gson.Gson;
import org.apache.commons.cli.*;

import java.io.FileInputStream;
import java.io.FileWriter;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.zip.ZipInputStream;

public class Main {
    public static void main(String[] args) throws Exception {
        // create the command line parser
        var parser = new DefaultParser();

        var options = new Options();
        options.addRequiredOption("i", "input-path", true, "");
        options.addRequiredOption("o", "output-path", true, "");
        options.addRequiredOption("m", "model-path", true, "");


        var line = parser.parse(options, args);

        var inputPath = line.getOptionValue("i");
        var outputPath = line.getOptionValue("o");
        var modelPath = line.getOptionValue("m");

        var classifier = new Classifier(modelPath);
        var zis = new ZipInputStream(new FileInputStream(inputPath));

        var outputGson = new Gson();
        var outputList = new ArrayList<>();

        var zipEntry = zis.getNextEntry();
        while (zipEntry != null) {
            var bytes = zis.readAllBytes();
            var gson = new Gson();
            var workload = gson.fromJson(new String(bytes), Workload.class);

            for (int i = 0; i < workload.count; i++) {
                var input = workload.inputs.get(i);
                var data = input.data;

                var startTime = System.nanoTime();

                var output = classifier.classify(data);

                var stopTime = System.nanoTime();
                var usDuration = (stopTime - startTime) / 1000;

                var outputObj = new Output();
                outputObj.o = output;
                outputObj.d = usDuration;
                outputObj.du = "us";
                outputObj.eo = input.expected_output;
                outputObj.iid = input.id;
                outputList.add(outputObj);

                if (outputList.size() % 1000 == 0) {
                    System.out.print(String.format("\r%d registered...", outputList.size()));
                }
            }

            zipEntry = zis.getNextEntry();
        }
        zis.closeEntry();
        zis.close();

        System.out.println("\nSaving!");
        var writer = new FileWriter(Paths.get(outputPath, "java_onnx_off.json").toString());
        outputGson.toJson(outputList, writer);
        writer.flush();
        writer.close();

        System.out.println("Done!");
    }
}
