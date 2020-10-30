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
        int gpuDeviceId = 0; // The GPU device ID to execute on
        var sessionOptions = new OrtSession.SessionOptions();
        sessionOptions.addCUDA(gpuDeviceId);
        session = environment.createSession(modelPath, sessionOptions);
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
}