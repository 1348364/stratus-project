import java.lang.instrument.Instrumentation;import java.nio.file.*;import java.lang.reflect.*;import java.util.concurrent.Executor;
public class FinalState1611{
 static Object call(Object o,String n,Object...v)throws Exception{for(Method m:o.getClass().getMethods())if(m.getName().equals(n)&&m.getParameterCount()==v.length)return m.invoke(o,v);throw new NoSuchMethodException(n);}
 public static void agentmain(String dir,Instrumentation i)throws Exception{
 Path w=Path.of(dir);if(!w.toString().endsWith("work/stratus-refine-1611")||!Path.of(System.getProperty("user.dir")).equals(Path.of(System.getProperty("user.home"),"Library/Application Support/ModrinthApp/profiles/Minecraft (1)")))throw new SecurityException();
 Class<?> mc=null;for(Class<?> c:i.getAllLoadedClasses())if(c.getName().equals("net.minecraft.class_310")){mc=c;break;}
 Object client=mc.getMethod("method_1551").invoke(null);
 ((Executor)client).execute(()->{try{
 Object server=call(client,"method_1576");if(!call(call(server,"method_27728"),"method_150").equals("Stratus Terrain Lab"))throw new SecurityException();
 Object p=client.getClass().getField("field_1724").get(client),o=client.getClass().getField("field_1690").get(client),abilities=call(p,"method_31549"),screen=client.getClass().getField("field_1755").get(client);
 StringBuilder text=new StringBuilder("position="+call(p,"method_23317")+","+call(p,"method_23318")+","+call(p,"method_23321")+"\nyaw="+call(p,"method_36454")+"\npitch="+call(p,"method_36455")+"\nhud="+o.getClass().getField("field_1842").get(o)+"\npause="+o.getClass().getField("field_1837").get(o)+"\nflying="+abilities.getClass().getField("field_7479").get(abilities)+"\nscreen="+(screen==null?"null":screen.getClass().getName())+"\n");
 Object world=client.getClass().getField("field_1687").get(client);
 try{text.append("worldTime="+call(world,"method_8532")+"\nrainGradient="+call(world,"method_8430",1.0f)+"\n");}catch(Exception e){text.append("worldMetadata=unavailable\n");}
 Files.writeString(w.resolve("final-client-state-v2.txt"),text.toString());
 }catch(Throwable e){try{Files.writeString(w.resolve("final-state-error.txt"),e.toString());}catch(Exception ignored){}}});
 }}