import java.lang.instrument.Instrumentation;import java.lang.reflect.*;import java.nio.file.*;import java.util.concurrent.Executor;
public final class ActiveBenchmark1611 {
 static Object call(Object o,String n,Object...a)throws Exception{for(Method m:o.getClass().getMethods())if(m.getName().equals(n)&&m.getParameterCount()==a.length){m.setAccessible(true);return m.invoke(o,a);}throw new NoSuchMethodException(n);}
 public static void agentmain(String dir,Instrumentation ins)throws Exception{
 Path w=Path.of(dir);if(!w.toString().endsWith("work/stratus-refine-1611")||!Path.of(System.getProperty("user.dir")).equals(Path.of(System.getProperty("user.home"),"Library/Application Support/ModrinthApp/profiles/Minecraft (1)")))throw new SecurityException();Class<?> mc=null;for(Class<?> c:ins.getAllLoadedClasses())if(c.getName().equals("net.minecraft.class_310")){mc=c;break;}ClassLoader cl=mc.getClassLoader();Object client=mc.getMethod("method_1551").invoke(null);
 Thread t=new Thread(()->{try{while(!Files.exists(w.resolve("activity-stop.txt"))){((Executor)client).execute(()->{try{
 Object server=call(client,"method_1576");if(server==null||!call(call(server,"method_27728"),"method_150").equals("Stratus Terrain Lab"))return;
 Class<?> glfw=cl.loadClass("org.lwjgl.glfw.GLFW");long win=(Long)call(call(client,"method_22683"),"method_4490");int focus=(Integer)glfw.getMethod("glfwGetWindowAttrib",long.class,int.class).invoke(null,win,0x00020001);
 Object limiter=call(client,"method_61964");String before=call(limiter,"method_66514").toString();int cap=(Integer)call(limiter,"method_61937");
 if(focus==1){call(limiter,"method_61939");cl.loadClass("dynamic_fps.impl.feature.state.IdleHandler").getMethod("onActivity").invoke(null);}
 Object player=client.getClass().getField("field_1724").get(client);Object world=client.getClass().getField("field_1687").get(client);
 Class<?> dynamic=cl.loadClass("dynamic_fps.impl.DynamicFPSMod");
 String row="time="+System.currentTimeMillis()+" focus="+focus+" limiter_before="+before+" cap_before="+cap+" limiter_after="+call(limiter,"method_66514")+" cap_after="+call(limiter,"method_61937")+" dynamic="+dynamic.getMethod("powerState").invoke(null)+" idle="+cl.loadClass("dynamic_fps.impl.feature.state.IdleHandler").getMethod("isIdle").invoke(null)+" position="+call(player,"method_23317")+","+call(player,"method_23318")+","+call(player,"method_23321")+" yaw="+call(player,"method_36454")+" pitch="+call(player,"method_36455")+" worldTime="+call(world,"method_8532")+" rain="+call(world,"method_8430",1.0f)+"\n";
 Files.writeString(w.resolve("activity-monitor.txt"),row,StandardOpenOption.CREATE,StandardOpenOption.APPEND);
 }catch(Throwable e){try{Files.writeString(w.resolve("activity-error.txt"),e.toString());}catch(Exception ignored){}}});Thread.sleep(5000);}Files.writeString(w.resolve("activity-stopped.txt"),"Temporary active-game benchmark timer stopped; saved settings were not changed.\n");}catch(Exception e){e.printStackTrace();}},"Stratus-active-benchmark-timer");t.setDaemon(true);t.start();
 }
}
