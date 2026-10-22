import java.lang.instrument.*;import java.security.ProtectionDomain;import java.nio.file.*;import java.util.*;import java.util.concurrent.*;import java.lang.reflect.*;import java.util.jar.JarFile;import org.objectweb.asm.*;
public final class ProfileAgent1610B {
 static Object call(Object o,String n,Object...a)throws Exception{for(Method m:o.getClass().getMethods())if(m.getName().equals(n)&&m.getParameterCount()==a.length)return m.invoke(o,a);throw new NoSuchMethodException(n);}
 public static void agentmain(String directory,Instrumentation ins)throws Exception{
  Path w=Path.of(directory);if(!w.toString().endsWith("work/stratus-refine-1610")||!Path.of(System.getProperty("user.dir")).equals(Path.of(System.getProperty("user.home"),"Library/Application Support/ModrinthApp/profiles/Minecraft (1)")))throw new SecurityException();
  String[] names={"net.irisshaders.iris.pipeline.CompositeRenderer$Pass","net.irisshaders.iris.pipeline.CompositeRenderer","net.irisshaders.iris.pipeline.FinalPassRenderer"};List<Class<?>> targets=new ArrayList<>();Class<?> mc=null;
  for(Class<?> c:ins.getAllLoadedClasses()){if(c.getName().equals("net.minecraft.class_310"))mc=c;for(String n:names)if(c.getName().equals(n))targets.add(c);}
  if(mc==null||targets.size()!=3||!ins.isRetransformClassesSupported())throw new IllegalStateException("Required exact Iris classes/retransform support unavailable");Object client=mc.getMethod("method_1551").invoke(null);ClassLoader cl=mc.getClassLoader();
  Object server=call(client,"method_1576");if(server==null||!call(call(server,"method_27728"),"method_150").equals("Stratus Terrain Lab"))throw new SecurityException();
  ins.appendToBootstrapClassLoaderSearch(new JarFile(w.resolve("agent/profile-hook-b.jar").toFile()));Class<?> hook=Class.forName("ProfileHook1610B",true,null);hook.getMethod("init",ClassLoader.class,String.class).invoke(null,cl,w.resolve("gpu-profile-b.json").toString());
  ClassFileTransformer transformer=new ClassFileTransformer(){public byte[] transform(ClassLoader loader,String name,Class<?> c,ProtectionDomain domain,byte[] bytes){
   if(!Arrays.asList(names).contains(name.replace('/','.')))return null;
   ClassReader reader=new ClassReader(bytes);ClassWriter writer=new ClassWriter(reader,ClassWriter.COMPUTE_MAXS);
   reader.accept(new ClassVisitor(Opcodes.ASM9,writer){public MethodVisitor visitMethod(int access,String method,String desc,String sig,String[] exceptions){MethodVisitor parent=super.visitMethod(access,method,desc,sig,exceptions);
    boolean pass=name.endsWith("$Pass")&&method.equals("setupState")&&desc.equals("()V");boolean renderer=name.endsWith("/CompositeRenderer")&&method.equals("renderAll")&&desc.equals("()V");boolean last=name.endsWith("/FinalPassRenderer")&&method.equals("renderFinalPass")&&desc.equals("()V");if(!pass&&!renderer&&!last)return parent;
    return new MethodVisitor(Opcodes.ASM9,parent){public void visitCode(){super.visitCode();if(pass){super.visitVarInsn(Opcodes.ALOAD,0);super.visitFieldInsn(Opcodes.GETFIELD,name,"name","Ljava/lang/String;");super.visitMethodInsn(Opcodes.INVOKESTATIC,"ProfileHook1610B","begin","(Ljava/lang/String;)V",false);}else if(last){super.visitLdcInsn("final");super.visitMethodInsn(Opcodes.INVOKESTATIC,"ProfileHook1610B","begin","(Ljava/lang/String;)V",false);}}
     public void visitInsn(int opcode){if((renderer||last)&&opcode==Opcodes.RETURN)super.visitMethodInsn(Opcodes.INVOKESTATIC,"ProfileHook1610B","end","()V",false);super.visitInsn(opcode);}};
   }},0);return writer.toByteArray();
  }};
  ins.addTransformer(transformer,true);ins.retransformClasses(targets.toArray(Class<?>[]::new));
  Thread worker=new Thread(()->{try{Thread.sleep(12000);CompletableFuture<Void> done=new CompletableFuture<>();((Executor)client).execute(()->{try{hook.getMethod("complete").invoke(null);done.complete(null);}catch(Throwable e){done.completeExceptionally(e);}});done.get(30,TimeUnit.SECONDS);}catch(Throwable e){try{Files.writeString(w.resolve("gpu-profile-error.txt"),e.toString());}catch(Exception ignored){}}finally{ins.removeTransformer(transformer);try{ins.retransformClasses(targets.toArray(Class<?>[]::new));Files.writeString(w.resolve("gpu-profile-b-restored.txt"),"Original bytecode restored for three Iris diagnostic targets; no game class or file changed.\n");}catch(Exception e){try{Files.writeString(w.resolve("gpu-profile-restore-error.txt"),e.toString());}catch(Exception ignored){}}}},"Stratus-GPU-profile-cleanup");worker.setDaemon(true);worker.start();
 }
}
