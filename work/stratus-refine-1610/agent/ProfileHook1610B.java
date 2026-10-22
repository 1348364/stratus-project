import java.lang.reflect.*;import java.nio.file.*;import java.util.*;
/** Temporary diagnostic only. No shader, game data, render state or settings writes. */
public final class ProfileHook1610B {
 private static Method gen,startQuery,endQuery,currentQuery,get,delete,finish;
 private static boolean enabled;private static String active;private static int begin;
 private static final List<Object[]> pending=new ArrayList<>();private static Path output;
 public static void init(ClassLoader cl,String path)throws Exception{
  Class<?> gl15=cl.loadClass("org.lwjgl.opengl.GL15C"),gl33=cl.loadClass("org.lwjgl.opengl.GL33C");
  gen=gl15.getMethod("glGenQueries");startQuery=gl15.getMethod("glBeginQuery",int.class,int.class);endQuery=gl15.getMethod("glEndQuery",int.class);currentQuery=gl15.getMethod("glGetQueryi",int.class,int.class);get=gl33.getMethod("glGetQueryObjectui64",int.class,int.class);delete=gl15.getMethod("glDeleteQueries",int.class);finish=cl.loadClass("org.lwjgl.opengl.GL11C").getMethod("glFinish");output=Path.of(path);enabled=true;
 }
 public static void begin(String label){if(!enabled)return;try{end();active=label;if((Integer)currentQuery.invoke(null,0x88BF,0x8865)!=0)throw new IllegalStateException("Another timer query is active");begin=(Integer)gen.invoke(null);startQuery.invoke(null,0x88BF,begin);}catch(Throwable e){fail(e);}}
 public static void end(){if(!enabled||active==null)return;try{endQuery.invoke(null,0x88BF);pending.add(new Object[]{active,begin});active=null;}catch(Throwable e){fail(e);}}
 private static void fail(Throwable e){enabled=false;try{Files.writeString(output.resolveSibling("gpu-profile-error.txt"),e.toString());}catch(Exception ignored){}}
 public static void complete()throws Exception{
  end();enabled=false;finish.invoke(null);StringBuilder out=new StringBuilder("{\"scope\":\"Actual Iris composite GL_TIME_ELAPSED intervals; diagnostic instrumentation overhead, not gameplay FPS\",\"samples\":[");int i=0;
  for(Object[] row:pending){long elapsed=(Long)get.invoke(null,(Integer)row[1],0x8866);if(i++>0)out.append(',');out.append("{\"pass\":\"").append(row[0]).append("\",\"gpu_ms\":").append(elapsed/1e6).append('}');delete.invoke(null,(Integer)row[1]);}
  out.append("]}\n");Files.writeString(output,out.toString());pending.clear();
 }
}
