public class Main {
    public static void main( String[] args ) throws Exception {
        Classifier classifier = new Classifier("/home/mikaelmello/Personal/tcc/src/runners/python/onnx/off");

        var input = new float[]{1,2,3,4,5,6,7};

        for (int i = 0; i < 100000; i++) {
            var startTime = System.nanoTime();
            classifier.classify(input);
            var stopTime = System.nanoTime();
            var duration = stopTime - startTime;

            System.out.println(duration);
        }
    }
}
