import java.lang.instrument.Instrumentation;import java.nio.file.*;import java.lang.reflect.*;import java.util.concurrent.Executor;
public class RestoreCameraRc2{
 static Object call(Object o,String n,Object...v)throws Exception{for(Method m:o.getClass().getMethods())if(m.getName().equals(n)&&m.getParameterCount()==v.length)return m.invoke(o,v);throw new NoSuchMethodException(n);}
 public static void agentmain(String dir,Instrumentation i)throws Exception{
 Path w=Path.of(dir);if(!w.toString().endsWith("work/stratus-170-rc2")||!Path.of(System.getProperty("user.dir")).equals(Path.of(System.getProperty("user.home"),"Library/Application Support/ModrinthApp/profiles/Minecraft (1)")))throw new SecurityException();
 Class<?> mc=null;for(Class<?> c:i.getAllLoadedClasses())if(c.getName().equals("net.minecraft.class_310")){mc=c;break;}
 Object client=mc.getMethod("method_1551").invoke(null);
 ((Executor)client).execute(()->{try{
 Object server=call(client,"method_1576");if(!call(call(server,"method_27728"),"method_150").equals("Stratus Terrain Lab"))throw new SecurityException();
 ((Executor)server).execute(()->{try{Object manager=call(server,"method_3734"),source=call(server,"method_3739");call(manager,"method_44252",source,"tp @p 160.47673452550254 65.00000584267644 41.747860878782795 3260.5178 54.589382");Files.writeString(w.resolve("camera-restore-command.txt"),"Original exact saved position/yaw/pitch restored through server teleport.\n");}catch(Exception e){throw new RuntimeException(e);}});
 
 }catch(Throwable e){try{Files.writeString(w.resolve("final-state-error.txt"),e.toString());}catch(Exception ignored){}}});
 }}