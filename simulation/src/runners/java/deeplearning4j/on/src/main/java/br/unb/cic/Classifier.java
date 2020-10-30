package br.unb.cic;

import org.deeplearning4j.nn.modelimport.keras.KerasModelImport;
import org.deeplearning4j.nn.multilayer.MultiLayerNetwork;
import org.nd4j.linalg.factory.Nd4j;

import java.nio.file.Paths;

public class Classifier {
    private final MultiLayerNetwork model;

    public Classifier(String modelDir) throws Exception {
        var modelPath = Paths.get(modelDir, "model.h5").toString();
        this.model = KerasModelImport.importKerasSequentialModelAndWeights(modelPath);
    }

    public int classify(float[][] testData) {
        var input = Nd4j.create(testData);
        var x = model.output(input);
        if (x.getColumn(0).getDouble(0) >= x.getColumn(1).getDouble(0) && x.getColumn(0).getDouble(0) >= x.getColumn(2).getDouble(0)) return 0;
        if (x.getColumn(1).getDouble(0) >= x.getColumn(0).getDouble(0) && x.getColumn(1).getDouble(0) >= x.getColumn(2).getDouble(0)) return 1;
        return 2;
    }
}