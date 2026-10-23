import java.lang.instrument.Instrumentation;import java.lang.reflect.*;import java.nio.file.*;import java.util.*;import java.util.concurrent.*;
public class RecoverFixtureRc2{
 static Object call(Object o,String n,Object...a)throws Exception{for(Method m:o.getClass().getMethods())if(m.getName().equals(n)&&m.getParameterCount()==a.length){m.setAccessible(true);return m.invoke(o,a);}throw new NoSuchMethodException(n);}
 public static void agentmain(String dir,Instrumentation ins)throws Exception{Path w=Path.of(dir);if(!w.toString().endsWith("work/stratus-170-rc2")||!Path.of(System.getProperty("user.dir")).equals(Path.of(System.getProperty("user.home"),"Library/Application Support/ModrinthApp/profiles/Minecraft (1)")))throw new SecurityException();Class<?> mc=null;for(Class<?> c:ins.getAllLoadedClasses())if(c.getName().equals("net.minecraft.class_310")){mc=c;break;}Object client=mc.getMethod("method_1551").invoke(null);ClassLoader cl=mc.getClassLoader();Object server=call(client,"method_1576");if(!call(call(server,"method_27728"),"method_150").equals("Stratus Terrain Lab"))throw new SecurityException();((Executor)server).execute(()->{try{
 if(!Files.exists(w.resolve("fixture-original.txt")))throw new SecurityException("Missing original snapshot");
 Object world=call(server,"method_30002"),manager=call(server,"method_3734"),source=call(server,"method_3739");Class<?> pos=cl.loadClass("net.minecraft.class_2338");Constructor<?> ctor=pos.getConstructor(int.class,int.class,int.class);Method get=world.getClass().getMethod("method_8320",pos);
 Class<?> entityType=cl.loadClass("net.minecraft.class_1297");
 List<Method> getters=new ArrayList<>();StringBuilder methods=new StringBuilder();
 for(Method m:world.getClass().getMethods())if(m.getParameterCount()==1&&m.getParameterTypes()[0]==UUID.class){methods.append(m.toString()).append("\n");if(entityType.isAssignableFrom(m.getReturnType()))getters.add(m);}
 Files.writeString(w.resolve("recovery-uuid-methods.txt"),methods.toString());
 if(getters.size()!=1)throw new IllegalStateException("Expected one Entity UUID lookup, found "+getters.size());
 Method lookup=getters.get(0);long most=((long)3245321<<32)|(6789864&0xffffffffL),least=((long)3456743<<32)|(6789745&0xffffffffL);UUID id=new UUID(most,least);
 Object sheep=lookup.invoke(world,id);if(sheep!=null){double x=((Number)call(sheep,"method_23317")).doubleValue(),z=((Number)call(sheep,"method_23321")).doubleValue();if(x<4200||x>4218||z<4200||z>4213)throw new SecurityException("Test sheep moved outside fixture");call(sheep,"method_31472");}
 if(lookup.invoke(world,id)!=null)throw new IllegalStateException("Sheep still present");
 call(manager,"method_44252",source,"fill 4200 160 4200 4217 172 4212 minecraft:air replace");
 StringBuilder after=new StringBuilder();for(int x=4200;x<=4217;x++)for(int y=160;y<=172;y++)for(int z=4200;z<=4212;z++)after.append(x+","+y+","+z+"="+get.invoke(world,ctor.newInstance(x,y,z))+"\n");
 if(!after.toString().equals(Files.readString(w.resolve("fixture-original.txt"))))throw new IllegalStateException("Original volume mismatch");
 Files.writeString(w.resolve("fixture-restored.txt"),after.toString());Files.writeString(w.resolve("fixture-stopped.txt"),"Recovered exact original 3042 air blocks; UUID sheep absent. Original watcher ended after its recorded failure. Recovery ran once on server thread.\n");
 
 }catch(Exception e){try{Files.writeString(w.resolve("recovery-error.txt"),e.toString());}catch(Exception ignored){}e.printStackTrace();}});}
}
