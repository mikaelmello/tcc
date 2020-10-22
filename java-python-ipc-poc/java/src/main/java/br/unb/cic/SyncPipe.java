package br.unb.cic;

import java.io.InputStream;
import java.io.OutputStream;

public class SyncPipe implements Runnable
{
    /**
     * This class pipes the output of your command to any new input you generated
     * with stdin. For example, suppose you run cp /mnt/c/a.txt /mnt/b/
     * but for some reason you are prompted: "do you really want to copy there yes/no?
     * then you can answer yes since your input is piped to the output of your
     * original command. (At least that is my practical interpretation might be wrong.)
     * @param istrm
     * @param ostrm
     */
    public SyncPipe(InputStream istrm, OutputStream ostrm) {
        istrm_ = istrm;
        ostrm_ = ostrm;
    }
    public void run() {

        try
        {
            final byte[] buffer = new byte[1024];
            for (int length = 0; (length = istrm_.read(buffer)) != -1; )
            {
                ostrm_.write(buffer, 0, length);
            }
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }
    private final OutputStream ostrm_;
    private final InputStream istrm_;
}