package qa;
import java.nio.file.*;
import java.util.*;
public final class FrameBench {
    private static String tag;
    private static long end,previous,window;
    private static java.lang.reflect.Method windowAttrib;
    private static int focusedFrames,unfocusedFrames,width,height;
    private static Object dynamicConfig;private static boolean dynamicEnabled;
    private static final ArrayList<Double> frames=new ArrayList<>();
    public static void start(String name,int seconds) {
        if(tag!=null)throw new IllegalStateException("Benchmark already active");
        try{
            Class<?> cfg=Class.forName("dynamic_fps.impl.config.DynamicFPSConfig");dynamicConfig=cfg.getField("INSTANCE").get(null);
            dynamicEnabled=(Boolean)cfg.getMethod("enabled").invoke(dynamicConfig);cfg.getMethod("setEnabled",boolean.class).invoke(dynamicConfig,false);
            Class.forName("dynamic_fps.impl.DynamicFPSMod").getMethod("onConfigChanged").invoke(null);
            System.out.println("[STRATUS_QA] Background frame limiter temporarily disabled for measurement; no config saved");
        }catch(Exception error){throw new IllegalStateException(error);}
        try{
            Object client=Class.forName("net.minecraft.class_310").getMethod("method_1551").invoke(null);
            Object win=client.getClass().getMethod("method_22683").invoke(client);
            window=(Long)win.getClass().getMethod("method_4490").invoke(win);
            Class<?> glfw=Class.forName("org.lwjgl.glfw.GLFW");
            windowAttrib=glfw.getMethod("glfwGetWindowAttrib",long.class,int.class);
            int[] w={0},h={0};glfw.getMethod("glfwGetFramebufferSize",long.class,int[].class,int[].class).invoke(null,window,w,h);
            width=w[0];height=h[0];focusedFrames=0;unfocusedFrames=0;
        }catch(Exception error){throw new IllegalStateException(error);}
        frames.clear();previous=0;end=System.nanoTime()+seconds*1000000000L;tag=name;
        System.out.println("[STRATUS_QA] BENCH_START "+name+" "+seconds);
    }
    public static void frame() {
        if(tag==null)return;
        try{if((Integer)windowAttrib.invoke(null,window,0x00020001)==1)focusedFrames++;else unfocusedFrames++;}
        catch(Exception error){unfocusedFrames++;}
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
            json=json.strip().replace("}",String.format(Locale.ROOT,",\"focused_frames\":%d,\"unfocused_frames\":%d,\"all_frames_focused\":%s,\"framebuffer\":[%d,%d],\"dynamic_fps_temporarily_disabled\":true}",focusedFrames,unfocusedFrames,unfocusedFrames==0,width,height))+"\n";
            Path out=Path.of(System.getProperty("stratus.qa.work"),"benchmarks");Files.createDirectories(out);Files.writeString(out.resolve(tag+".json"),json);
            System.out.println("[STRATUS_QA] BENCH_RESULT "+json.strip());
        } catch(Exception error) {error.printStackTrace();}
        try{dynamicConfig.getClass().getMethod("setEnabled",boolean.class).invoke(dynamicConfig,dynamicEnabled);Class.forName("dynamic_fps.impl.DynamicFPSMod").getMethod("onConfigChanged").invoke(null);}catch(Exception e){e.printStackTrace();}
        tag=null;
    }
}
