package br.unb.cic;

import ai.onnxruntime.NodeInfo;
import ai.onnxruntime.OnnxTensor;
import ai.onnxruntime.OrtEnvironment;
import ai.onnxruntime.OrtException;
import ai.onnxruntime.OrtSession;
import ai.onnxruntime.OrtSession.Result;

import java.nio.file.Paths;
import java.util.Collections;

import static java.lang.Math.round;

public class Classifier {
   private final OrtSession session;
   private final OrtEnvironment environment;
   private final String inputName;

    public Classifier(String modelDir) throws Exception {
        var modelPath = Paths.get(modelDir, "model.onnx").toString();
        environment = OrtEnvironment.getEnvironment();
        session = environment.createSession(modelPath);
        inputName = session.getInputNames().iterator().next();
    }

    public int classify(float[][] testData) throws OrtException {
        try (OnnxTensor test = OnnxTensor.createTensor(environment, testData);
             Result output = session.run(Collections.singletonMap(inputName, test))) {
            var x = (float[][])output.get(0).getValue();
            if (x[0][0] >= x[0][1] && x[0][0] >= x[0][2]) return 0;
            if (x[0][1] >= x[0][0] && x[0][1] >= x[0][2]) return 1;
            return 2;
        }
    }

    private static float[][] scaler(float[] values) {
        assert values.length == 7;

        float[][] scaled = { { 0, 0, 0, 0, 0, 0, 0 } };
        double[] scale = { 119.83552861, 1.42122914, 1.31913874, 12.90645335, 1283.0616716, 45.84544104, 11.46346616 };
        double[] mean = { 1.67900462e+02, 3.11090588e+00, 4.43886897e+00, 4.27830029e+01, 4.23752228e+03, 9.29964257e+01,
                3.18708094e+01 };

        for (int i = 0; i < 7; i++) {
            scaled[0][i] = (float) ((values[i] - mean[i]) / scale[i]);
        }

        return scaled;
    }
}