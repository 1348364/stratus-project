package qa;
import java.nio.file.*;
import java.util.*;
public final class FrameBench {
    private static String tag;
    private static long end,previous;
    private static final ArrayList<Double> frames=new ArrayList<>();
    public static void start(String name,int seconds) {
        if(tag!=null)throw new IllegalStateException("Benchmark already active");
        frames.clear();previous=0;end=System.nanoTime()+seconds*1000000000L;tag=name;
        System.out.println("[STRATUS_QA] BENCH_START "+name+" "+seconds);
    }
    public static void frame() {
        if(tag==null)return;
        long now=System.nanoTime();
        if(previous!=0)frames.add((now-previous)/1000000.0);
        previous=now;
        if(now<end)return;
        try {
            double[] sorted=frames.stream().mapToDouble(Double::doubleValue).sorted().toArray();
            if(sorted.length<3)throw new IllegalStateException("Too few rendered frames");
            double sum=0;for(double value:sorted)sum+=value;
            double mean=sum/sorted.length,median=sorted[sorted.length/2],p95=sorted[(int)((sorted.length-1)*.95)],p99=sorted[(int)((sorted.length-1)*.99)];
            int count=Math.max(1,(int)Math.ceil(sorted.length*.01));double slow=0;for(int i=sorted.length-count;i<sorted.length;i++)slow+=sorted[i];
            String json=String.format(Locale.ROOT,"{\"tag\":\"%s\",\"frames\":%d,\"sampled_seconds\":%.4f,\"average_fps\":%.4f,\"median_frame_ms\":%.4f,\"p95_frame_ms\":%.4f,\"p99_frame_ms\":%.4f,\"one_percent_low_fps\":%.4f,\"method\":\"MinecraftClient render-head to render-head monotonic wall intervals\"}\n",tag,sorted.length,sum/1000,1000/mean,median,p95,p99,1000/(slow/count));
            Path out=Path.of(System.getProperty("user.dir"),"benchmarks");Files.createDirectories(out);Files.writeString(out.resolve(tag+".json"),json);
            System.out.println("[STRATUS_QA] BENCH_RESULT "+json.strip());
        } catch(Exception error) {error.printStackTrace();}
        tag=null;
    }
}
