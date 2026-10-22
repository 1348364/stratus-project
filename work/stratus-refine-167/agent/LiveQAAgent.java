import java.lang.instrument.Instrumentation;
import java.nio.file.*;
import java.lang.reflect.*;
import java.io.File;
import java.util.concurrent.Executor;
import java.util.function.Consumer;
public final class LiveQAAgent {
 static Object call(Object o,String n,Object...a)throws Exception{for(Method m:o.getClass().getMethods())if(m.getName().equals(n)&&m.getParameterCount()==a.length)return m.invoke(o,a);throw new NoSuchMethodException(n);}
 public static void agentmain(String directory,Instrumentation instrumentation)throws Exception{
  Path work=Path.of(directory).toAbsolutePath();
  Path allowed=Path.of(System.getProperty("user.home"),"Library/Application Support/ModrinthApp/profiles/Minecraft (1)");
  if(!Path.of(System.getProperty("user.dir")).equals(allowed)||!work.toString().endsWith("work/stratus-refine-167"))throw new SecurityException("Unexpected game or evidence directory");
  Class<?> mc=null;for(Class<?> c:instrumentation.getAllLoadedClasses())if(c.getName().equals("net.minecraft.class_310")){mc=c;break;}
  if(mc==null)throw new IllegalStateException("Minecraft client is absent");
  Object client=mc.getMethod("method_1551").invoke(null);ClassLoader loader=mc.getClassLoader();
  ((Executor)client).execute(()->{try{
   Object server=call(client,"method_1576");if(server==null)throw new IllegalStateException("No integrated world");
   String world=(String)call(call(server,"method_27728"),"method_150");if(!world.equals("Stratus Terrain Lab"))throw new SecurityException("Only designated test world allowed");
   Object player=client.getClass().getField("field_1724").get(client);Object window=call(client,"method_22683");long handle=(Long)call(window,"method_4490");
   Object focused=loader.loadClass("org.lwjgl.glfw.GLFW").getMethod("glfwGetWindowAttrib",long.class,int.class).invoke(null,handle,0x00020001);
   Object pipeline=call(loader.loadClass("net.irisshaders.iris.Iris").getMethod("getPipelineManager").invoke(null),"getPipelineNullable");
   String state="world="+world+"\npipeline="+(pipeline==null?"none":pipeline.getClass().getName())+"\nfocused="+focused+"\nposition="+call(player,"method_23317")+","+call(player,"method_23318")+","+call(player,"method_23321")+"\nscreen="+client.getClass().getField("field_1755").get(client)+"\n";
   Files.writeString(work.resolve("live-read-only-state.txt"),state);
   Object framebuffer=call(client,"method_1522");
   loader.loadClass("net.minecraft.class_318").getMethod("method_22690",File.class,String.class,loader.loadClass("net.minecraft.class_276"),int.class,Consumer.class).invoke(null,work.toFile(),"baseline-current-view.png",framebuffer,1,(Consumer<Object>)message->{try{Files.writeString(work.resolve("live-read-only-complete.txt"),"Minecraft screenshot callback completed\n");}catch(Exception e){e.printStackTrace();}});
  }catch(Throwable error){try{Files.writeString(work.resolve("live-read-only-error.txt"),error.toString());}catch(Exception ignored){}error.printStackTrace();}});
 }
}
