import java.lang.instrument.Instrumentation;import java.nio.file.*;import java.lang.reflect.*;import java.util.*;import java.util.concurrent.Executor;import java.util.function.BiConsumer;
public class RecheckMetrics{
 static Object call(Object o,String n,Object...a)throws Exception{for(Method m:o.getClass().getMethods())if(m.getName().equals(n)&&m.getParameterCount()==a.length){m.setAccessible(true);return m.invoke(o,a);}throw new NoSuchMethodException(n);}
 public static void agentmain(String dir,Instrumentation ins)throws Exception{
 Path work=Path.of(dir);if(!Path.of(System.getProperty("user.dir")).equals(Path.of(System.getProperty("user.home"),"Library/Application Support/ModrinthApp/profiles/Minecraft (1)")))throw new SecurityException();if(!work.toString().endsWith("work/stratus-recheck-167"))throw new SecurityException();Class<?> mc=null;for(Class<?> c:ins.getAllLoadedClasses())if(c.getName().equals("net.minecraft.class_310")){mc=c;break;}
 Object client=mc.getMethod("method_1551").invoke(null);ClassLoader cl=mc.getClassLoader();((Executor)client).execute(()->{try{
 Object server=call(client,"method_1576");if(!call(call(server,"method_27728"),"method_150").equals("Stratus Terrain Lab"))throw new SecurityException();
 long win=(Long)call(call(client,"method_22683"),"method_4490");Class<?> glfw=cl.loadClass("org.lwjgl.glfw.GLFW");Object focus=glfw.getMethod("glfwGetWindowAttrib",long.class,int.class).invoke(null,win,0x00020001);int[] width={0},height={0};glfw.getMethod("glfwGetFramebufferSize",long.class,int[].class,int[].class).invoke(null,win,width,height);
 Class<?> iris=cl.loadClass("net.irisshaders.iris.Iris");Optional<?> pack=(Optional<?>)iris.getMethod("getCurrentPack").invoke(null);Object actual=pack.orElseThrow();List<String> profiles=new ArrayList<>();Object menu=call(actual,"getMenuContainer");Object profileSet=call(menu,"getProfiles");call(profileSet,"forEach",(BiConsumer<String,Object>)(name,p)->profiles.add(name));
 Object values=call(call(actual,"getShaderPackOptions"),"getOptionValues");StringBuilder out=new StringBuilder("focused="+focus+"\nframebuffer="+width[0]+"x"+height[0]+"\nprofiles="+profiles+"\nprofile_info="+call(actual,"getProfileInfo")+"\n");
 out.append("pipeline="+call(iris.getMethod("getPipelineManager").invoke(null),"getPipelineNullable").getClass().getName()+"\n");Object cfg=iris.getMethod("getIrisConfig").invoke(null);out.append("selected_pack="+call(cfg,"getShaderPackName")+"\n");
 for(String key:List.of("CLOUD_LAYERS","GROUND_WARMTH","MIST_DETAIL","REFLECTION_MODE","WATER_EXTINCTION","WATER_RENDER_QUALITY","WATER_TURBIDITY","CLOUD_STYLE","CIRRUS_AMOUNT","CIRRUS_ALTITUDE","CIRRUS_DENSITY","VANILLA_FACE_CONTRAST","REALISTIC_FACE_CONTRAST","SUN_CORE_BRIGHTNESS","SUN_HALO_STRENGTH","SUN_HALO_RADIUS"))out.append(key+"="+call(values,"getStringValueOrDefault",key)+"\n");
 try{Object dyn=cl.loadClass("dynamic_fps.impl.config.DynamicFPSConfig").getField("INSTANCE").get(null);out.append("DynamicFPS.enabled="+call(dyn,"enabled")+"\n");}catch(Exception e){out.append("DynamicFPS.state=unavailable\n");}
 Files.writeString(work.resolve("runtime-state.txt"),out.toString());
 }catch(Throwable e){try{Files.writeString(work.resolve("runtime-error.txt"),e.toString());}catch(Exception ignored){}e.printStackTrace();}});
 }
}
