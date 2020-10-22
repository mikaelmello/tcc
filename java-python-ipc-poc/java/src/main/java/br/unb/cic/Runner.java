package br.unb.cic;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.Collections;
import java.util.stream.Collectors;

public class Runner {
    private Process process;
    private OutputStream stdIn;
    private InputStream stdOut;

    public Runner() {}

    public void start() throws Exception {
        ProcessBuilder builder = new ProcessBuilder("python", "/home/mikaelmello/Personal/tcc/java-python-ipc-poc/service.py");

        process = builder.start();

        new Thread(new SyncPipe(process.getErrorStream(), System.err)).start();
        stdIn = process.getOutputStream();
        stdOut = process.getInputStream();

        int var = 2;

        var inp = new float[27520]; // model's parameters length
        for (int i = 0; i < 27520; i++) {
            inp[i] = (i % 2 == 0 ? 0.0f : 1.0f);
        }

        for (int i = 0; i < 10000; i++) {
            long startTime = System.nanoTime();

            // 27520 parameters = 27520B (or 26.875KB) in the best possible case

            // trivial serialization gives 4 bytes per value + 4 bytes for the length
            // 11080B = 107.5KB
            write(inp);

            // 1B
            read();

            long stopTime = System.nanoTime();
            System.out.println(stopTime-startTime);
        }
    }

    // 27520 B / 0.00002s = X B/s

    private int read() throws IOException {
        return stdOut.read();
    }

    private void write(float[] input) throws IOException {
        byte[] size = long2ByteArray(input.length);
        stdIn.write(size);

        for (float v : input) {
            byte[] val = float2ByteArray(v);
            stdIn.write(val);
        }
        stdIn.flush();
    }

    private static byte[] long2ByteArray(int value) {
        return ByteBuffer.allocate(4).putInt(value).array();
    }

    private static byte[] float2ByteArray(float value) {
        return ByteBuffer.allocate(4).putFloat(value).array();
    }
}
