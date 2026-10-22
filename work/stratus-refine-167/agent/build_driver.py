from pathlib import Path
import re,subprocess,zipfile
w=Path(__file__).parent;s=Path('work/stratus-main-qa/helper/StratusVisualQA.java').read_text()
s=s.replace('import net.fabricmc.api.ClientModInitializer;','import java.lang.instrument.Instrumentation;')
s=s.replace('public final class StratusVisualQA implements ClientModInitializer {','''public final class LiveRunAgent {
    private static ClassLoader gameLoader;
    private static Path work;
    private volatile boolean stopped;
    private Object originalScreen;
    private boolean originalHud,originalPause;
    public static void agentmain(String directory,Instrumentation instrumentation)throws Exception{
        work=Path.of(directory).toAbsolutePath();
        for(Class<?> c:instrumentation.getAllLoadedClasses())if(c.getName().equals("net.minecraft.class_310")){gameLoader=c.getClassLoader();break;}
        if(gameLoader==null)throw new IllegalStateException("No client");
        new LiveRunAgent().onInitializeClient();
    }
''')
s=s.replace('Path.of(System.getProperty("stratus.qa.work")).toAbsolutePath()','work')
s=s.replace('!actualGame.toString().equals(System.getProperty("stratus.qa.authorizedGame")) || !game.toString().endsWith("work/stratus-main-qa")','!actualGame.equals(Path.of(System.getProperty("user.home"),"Library/Application Support/ModrinthApp/profiles/Minecraft (1)")) || !game.toString().endsWith("work/stratus-refine-167")')
s=s.replace('while (true) {','while (!stopped) {').replace('Class.forName(', 'gameLoader.loadClass(').replace('STRATUS_QA','STRATUS_QA167')
needle='''                Object options = client.getClass().getField("field_1690").get(client);
                options.getClass().getField("field_1842").setBoolean(options, true);'''
replacement='''                Object options = client.getClass().getField("field_1690").get(client);
                originalScreen=client.getClass().getField("field_1755").get(client);
                originalHud=options.getClass().getField("field_1842").getBoolean(options);
                originalPause=options.getClass().getField("field_1837").getBoolean(options);
                Object currentPlayer=client.getClass().getField("field_1724").get(client);
                String snapshot="position="+call(currentPlayer,"method_23317")+","+call(currentPlayer,"method_23318")+","+call(currentPlayer,"method_23321")+"\\nyaw="+call(currentPlayer,"method_36454")+"\\npitch="+call(currentPlayer,"method_36455")+"\\nhud="+originalHud+"\\npause="+originalPause+"\\n";
                Files.writeString(game.resolve("original-client-state.txt"),snapshot);
                options.getClass().getField("field_1842").setBoolean(options, true);'''
assert needle in s;s=s.replace(needle,replacement)
s=s.replace('"tp ShaderCheck "+coordinates','"tp @p "+coordinates')
s=s.replace('Object player=call(call(server,"method_3760"),"method_14566","ShaderCheck");','''Object cp=client.getClass().getField("field_1724").get(client);
                            java.util.UUID uuid=(java.util.UUID)call(cp,"method_5667");
                            Object pm=call(server,"method_3760"),player=null;
                            Class<?> serverPlayer=gameLoader.loadClass("net.minecraft.class_3222");
                            for(Method method:pm.getClass().getMethods())if(method.getParameterCount()==1&&method.getParameterTypes()[0]==java.util.UUID.class&&serverPlayer.isAssignableFrom(method.getReturnType())){player=method.invoke(pm,uuid);break;}
                            if(player==null)throw new IllegalStateException("No test player");''')
a=s.index('                case "BENCH" ->');b=s.index('                case "MENU" ->',a)
s=s[:a]+'''                case "STOP" -> {
                    Object options=client.getClass().getField("field_1690").get(client);
                    options.getClass().getField("field_1842").setBoolean(options,originalHud);
                    options.getClass().getField("field_1837").setBoolean(options,originalPause);
                    call(client,"method_1507",originalScreen);
                    stopped=true;
                    Files.writeString(game.resolve("driver-stopped.txt"),"Restored HUD/pause/menu; polling stopped.\\n");
                }
'''+s[b:]
(w/'LiveRunAgent.java').write_text(s)
subprocess.run(['javac','--release','21','-d',str(w/'classes'),str(w/'LiveRunAgent.java')],check=True)
with zipfile.ZipFile(w/'live-run-agent.jar','w') as z:
 z.writestr('META-INF/MANIFEST.MF','Manifest-Version: 1.0\nAgent-Class: LiveRunAgent\n\n')
 for p in (w/'classes').glob('LiveRunAgent*.class'):z.write(p,p.name)
