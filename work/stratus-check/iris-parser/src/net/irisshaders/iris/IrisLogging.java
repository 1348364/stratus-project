package net.irisshaders.iris;
public final class IrisLogging {
    public void error(String text) { System.err.println(text); }
    public void error(String text, Throwable error) { System.err.println(text); }
    public void warn(String text) { System.err.println(text); }
}
