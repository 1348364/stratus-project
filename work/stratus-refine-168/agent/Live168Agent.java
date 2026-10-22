import java.lang.instrument.Instrumentation;
import java.io.File;
import java.lang.reflect.*;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.function.Consumer;

/** Test-only Minecraft API driver. Installed solely in the isolated copied world. */
public final class Live168Agent {
    private static ClassLoader gameLoader;
    private static Path work;
    private volatile boolean stopped;
    private Object originalScreen;
    private boolean originalHud,originalPause,originalFlying;
    private boolean vanillaCapture;
    public static void agentmain(String directory,Instrumentation instrumentation)throws Exception{
        work=Path.of(directory).toAbsolutePath();
        for(Class<?> c:instrumentation.getAllLoadedClasses())if(c.getName().equals("net.minecraft.class_310")){gameLoader=c.getClassLoader();break;}
        if(gameLoader==null)throw new IllegalStateException("No client");
        new Live168Agent().onInitializeClient();
    }

    private final Path actualGame = Path.of(System.getProperty("user.dir")).toAbsolutePath();
    private final Path game = work;
    private final Queue<String> actions = new ArrayDeque<>();
    private long resumeAt = 0;
    private Object client;
    private boolean initialized;
    private volatile boolean awaitingCommand;
    private double[] expectedCamera;

    public void onInitializeClient() {
        if (!actualGame.equals(Path.of(System.getProperty("user.home"),"Library/Application Support/ModrinthApp/profiles/Minecraft (1)")) || !game.toString().endsWith("work/stratus-refine-168")) throw new IllegalStateException("QA helper requires explicit Main test launch");
        Thread worker = new Thread(() -> {
            while (!stopped) {
                try {
                    Thread.sleep(750);
                    client = gameLoader.loadClass("net.minecraft.class_310").getMethod("method_1551").invoke(null);
                    ((Executor)client).execute(this::poll);
                } catch (Throwable error) { System.out.println("[STRATUS_QA168] WAIT " + error); }
            }
        }, "Stratus-visual-QA");
        worker.setDaemon(true); worker.start();
    }
    private Object call(Object receiver, String name, Object... args) throws Exception {
        for (Method method : receiver.getClass().getMethods()) {
            if (method.getName().equals(name) && method.getParameterCount() == args.length) return method.invoke(receiver, args);
        }
        throw new NoSuchMethodException(name);
    }
    private void requireShader() throws Exception {
        Object manager=gameLoader.loadClass("net.irisshaders.iris.Iris").getMethod("getPipelineManager").invoke(null);
        Object pipeline=call(manager,"getPipelineNullable");
        if(pipeline==null||!pipeline.getClass().getName().contains("IrisRenderingPipeline")){
            actions.clear();throw new IllegalStateException("Shader pipeline failed; capture queue stopped");
        }
        System.out.println("[STRATUS_QA168] VERIFIED_PIPELINE "+pipeline.getClass().getName());
    }
    private void poll() {
        try {
            Object server = call(client, "method_1576");
            if (server == null || client.getClass().getField("field_1724").get(client) == null) return;
            String levelName=(String)call(call(server,"method_27728"),"method_150");
            if(!levelName.equals("Stratus Terrain Lab")) {actions.clear();return;}
            if (!initialized) {
                Object options = client.getClass().getField("field_1690").get(client);
                originalScreen=client.getClass().getField("field_1755").get(client);
                originalHud=options.getClass().getField("field_1842").getBoolean(options);
                originalPause=options.getClass().getField("field_1837").getBoolean(options);
                Object currentPlayer=client.getClass().getField("field_1724").get(client);
                originalFlying=call(currentPlayer,"method_31549").getClass().getField("field_7479").getBoolean(call(currentPlayer,"method_31549"));
                String snapshot="position="+call(currentPlayer,"method_23317")+","+call(currentPlayer,"method_23318")+","+call(currentPlayer,"method_23321")+"\nyaw="+call(currentPlayer,"method_36454")+"\npitch="+call(currentPlayer,"method_36455")+"\nhud="+originalHud+"\npause="+originalPause+"\nflying="+originalFlying+"\n";
                Files.writeString(game.resolve("original-client-state.txt"),snapshot);
                options.getClass().getField("field_1842").setBoolean(options, true);
                options.getClass().getField("field_1837").setBoolean(options, false);
                call(client,"method_1507",new Object[]{null});
                initialized = true;
                System.out.println("[STRATUS_QA168] READY: local world, HUD hidden");
            }
            Path request = game.resolve("qa-request.txt");
            if (Files.isRegularFile(request)) {
                for (String row : Files.readAllLines(request)) if (!row.isBlank() && !row.startsWith("#")) {
                    if(row.equals("CANCEL")){actions.clear();resumeAt=0;}else actions.add(row);
                }
                Files.move(request,game.resolve("qa-request-consumed.txt"),StandardCopyOption.REPLACE_EXISTING);
                System.out.println("[STRATUS_QA168] QUEUED " + actions.size());
            }
            // Waits and screenshots must start after the integrated server has
            // actually executed a command, rather than after it was enqueued.
            if (awaitingCommand || System.currentTimeMillis() < resumeAt || actions.isEmpty()) return;
            String row = actions.remove();
            String[] parts = row.split(" ", 2);
            String op = parts[0], argument = parts.length > 1 ? parts[1] : "";
            switch (op) {
                case "WAIT" -> resumeAt = System.currentTimeMillis() + Long.parseLong(argument) * 1000;
                case "CMD" -> {
                    awaitingCommand = true;
                    ((Executor)server).execute(() -> {
                    try {
                        Object manager = call(server, "method_3734"), source = call(server, "method_3739");
                        call(manager, "method_44252", source, argument);
                        System.out.println("[STRATUS_QA168] COMMAND " + argument);
                    } catch (Throwable error) { error.printStackTrace(); }
                    finally { awaitingCommand = false; }
                    });
                }
                case "CAM" -> {
                    String[] values=argument.split(" ");
                    expectedCamera=new double[]{Double.parseDouble(values[0]),Double.parseDouble(values[1]),Double.parseDouble(values[2])};
                    awaitingCommand=true;
                    ((Executor)server).execute(() -> {
                        try {
                            Object manager=call(server,"method_3734"),source=call(server,"method_3739");
                            String coordinates=String.format(java.util.Locale.ROOT,"%.4f %.4f %.4f %s %s",expectedCamera[0],expectedCamera[1],expectedCamera[2],values[3],values[4]);
                            call(manager,"method_44252",source,"tp @p "+coordinates);
                            Object cp=client.getClass().getField("field_1724").get(client);
                            java.util.UUID uuid=(java.util.UUID)call(cp,"method_5667");
                            Object pm=call(server,"method_3760"),player=null;
                            Class<?> serverPlayer=gameLoader.loadClass("net.minecraft.class_3222");
                            for(Method method:pm.getClass().getMethods())if(method.getParameterCount()==1&&method.getParameterTypes()[0]==java.util.UUID.class&&serverPlayer.isAssignableFrom(method.getReturnType())){player=method.invoke(pm,uuid);break;}
                            if(player==null)throw new IllegalStateException("No test player");
                            Object abilities=call(player,"method_31549");
                            abilities.getClass().getField("field_7479").setBoolean(abilities,true);
                            call(player,"method_7355");
                            System.out.println("[STRATUS_QA168] CAMERA "+coordinates+" creative-flight server confirmed");
                        } catch(Throwable error){error.printStackTrace();}
                        finally{awaitingCommand=false;}
                    });
                }
                case "SHOT" -> {
                    if(!argument.contains("-menu-")&&client.getClass().getField("field_1755").get(client)!=null){
                        call(client,"method_1507",new Object[]{null});
                        ((ArrayDeque<String>)actions).addFirst(row);resumeAt=System.currentTimeMillis()+2500;return;
                    }
                    if(!vanillaCapture)requireShader();
                    if(expectedCamera!=null){
                        Object player=client.getClass().getField("field_1724").get(client);
                        double[] actual={(Double)call(player,"method_23317"),(Double)call(player,"method_23318"),(Double)call(player,"method_23321")};
                        for(int i=0;i<3;i++)if(Math.abs(actual[i]-expectedCamera[i])>0.15){actions.clear();throw new IllegalStateException("Camera moved before capture: "+Arrays.toString(actual)+" expected "+Arrays.toString(expectedCamera));}
                        System.out.println("[STRATUS_QA168] VERIFIED_CAMERA "+Arrays.toString(actual));
                    }
                    Object framebuffer = call(client, "method_1522");
                    Method save = gameLoader.loadClass("net.minecraft.class_318").getMethod("method_22690", File.class,String.class,
                            gameLoader.loadClass("net.minecraft.class_276"),int.class,Consumer.class);
                    save.invoke(null,game.toFile(),argument+".png",framebuffer,1,(Consumer<Object>)text ->
                            System.out.println("[STRATUS_QA168] SCREENSHOT " + argument + " " + text));
                }
                case "RESUME" -> {
                    call(client,"method_1507",new Object[]{null});
                    resumeAt = System.currentTimeMillis()+1500;
                }
                case "FLY" -> {
                    Object player=client.getClass().getField("field_1724").get(client);
                    Object abilities=call(player,"method_31549");
                    abilities.getClass().getField("field_7479").setBoolean(abilities,true);
                    call(player,"method_7355");
                    System.out.println("[STRATUS_QA168] CREATIVE_FLIGHT_ENABLED");
                }
                case "HUD" -> {
                    Object options = client.getClass().getField("field_1690").get(client);
                    options.getClass().getField("field_1842").setBoolean(options, !argument.equals("show"));
                    System.out.println("[STRATUS_QA168] HUD " + argument);
                }
                case "VANILLA" -> {
                    Class<?> iris=gameLoader.loadClass("net.irisshaders.iris.Iris");
                    Object config=iris.getMethod("getIrisConfig").invoke(null);
                    call(config,"setShadersEnabled",false);call(config,"save");iris.getMethod("reload").invoke(null);
                    vanillaCapture=true;resumeAt=System.currentTimeMillis()+6000;
                }
                case "PACK" -> {
                    vanillaCapture=false;
                    Class<?> iris = gameLoader.loadClass("net.irisshaders.iris.Iris");
                    Object config = iris.getMethod("getIrisConfig").invoke(null);
                    call(config,"setShaderPackName",argument); call(config,"setShadersEnabled",true);
                    call(config,"save");
                    iris.getMethod("reload").invoke(null);
                    requireShader();
                    System.out.println("[STRATUS_QA168] PACK " + argument);
                    resumeAt = System.currentTimeMillis()+5000;
                }
                case "STOP" -> {
                    Object options=client.getClass().getField("field_1690").get(client);
                    options.getClass().getField("field_1842").setBoolean(options,originalHud);
                    options.getClass().getField("field_1837").setBoolean(options,originalPause);
                    call(client,"method_1507",originalScreen);
                    Object cp=client.getClass().getField("field_1724").get(client);
                    call(cp,"method_31549").getClass().getField("field_7479").setBoolean(call(cp,"method_31549"),originalFlying);
                    java.util.UUID uuid=(java.util.UUID)call(cp,"method_5667");
                    ((Executor)server).execute(()->{try{
                        Object pm=call(server,"method_3760");
                        Class<?> sp=gameLoader.loadClass("net.minecraft.class_3222");
                        for(Method m:pm.getClass().getMethods())if(m.getParameterCount()==1&&m.getParameterTypes()[0]==java.util.UUID.class&&sp.isAssignableFrom(m.getReturnType())){
                            Object player=m.invoke(pm,uuid),abilities=call(player,"method_31549");
                            abilities.getClass().getField("field_7479").setBoolean(abilities,originalFlying);call(player,"method_7355");break;
                        }
                    }catch(Exception error){error.printStackTrace();}});
                    stopped=true;
                    Files.writeString(game.resolve("driver-stopped.txt"),"Restored HUD/pause/menu; polling stopped.\n");
                }
                case "MENU" -> {
                    Class<?> screen=gameLoader.loadClass("net.irisshaders.iris.gui.screen.ShaderPackScreen");
                    Object parent=client.getClass().getField("field_1755").get(client);
                    Object created=screen.getConstructors()[0].newInstance(parent);
                    call(client,"method_1507",created);
                    System.out.println("[STRATUS_QA168] MENU "+created.getClass().getName());
                }
                case "OPTIONS" -> {
                    Object current=client.getClass().getField("field_1755").get(client);
                    if(argument.equals("root")){
                        Field switchField=current.getClass().getDeclaredField("screenSwitchButton");switchField.setAccessible(true);
                        Object button=switchField.get(current);
                        call(button,"method_25306",new Object[]{null});
                    }else{
                        Field nav=current.getClass().getDeclaredField("navigation");nav.setAccessible(true);
                        call(nav.get(current),"open",argument);
                    }
                    System.out.println("[STRATUS_QA168] OPTIONS "+argument);
                }
                case "WIDGET" -> {
                    Object current=client.getClass().getField("field_1755").get(client);
                    List<?> children=(List<?>)call(current,"method_25396");
                    boolean found=false;
                    for(Object child:children){
                        try{
                            String label=(String)call(call(child,"method_25369"),"getString");
                            System.out.println("[STRATUS_QA168] WIDGET "+child.getClass().getName()+" "+label);
                            if(label.equals(argument)){call(child,"method_25306",new Object[]{null});found=true;break;}
                        }catch(NoSuchMethodException ignored){}
                    }
                    if(!found)System.out.println("[STRATUS_QA168] WIDGET_NOT_FOUND "+argument);
                }
                case "STATE" -> {
                    Class<?> iris = gameLoader.loadClass("net.irisshaders.iris.Iris");
                    Object manager = iris.getMethod("getPipelineManager").invoke(null);
                    Object pipeline = call(manager,"getPipelineNullable");
                    for (Field field : pipeline.getClass().getDeclaredFields()) {
                        if (field.getType().getName().equals("net.irisshaders.iris.targets.RenderTargets")) {
                            field.setAccessible(true); Object targets=field.get(pipeline);
                            for(int i=0;i<8;i++) {
                                Object target=call(targets,"get",i);
                                System.out.println("[STRATUS_QA168] BUFFER "+i+" "+call(target,"getInternalFormat"));
                            }
                        }
                    }
                    Class<?> settings=gameLoader.loadClass("net.irisshaders.iris.shaderpack.materialmap.WorldRenderingSettings");
                    Object instance=settings.getField("INSTANCE").get(null);
                    Map<?,?> ids=(Map<?,?>)call(instance,"getBlockStateIds");
                    for(var entry:ids.entrySet()) {
                        String name=entry.getKey().toString();
                        if(name.startsWith("Block{minecraft:water}") || name.equals("Block{minecraft:stone}") || name.startsWith("Block{minecraft:iron_ore}") || name.startsWith("Block{minecraft:deepslate_iron_ore}"))
                            System.out.println("[STRATUS_QA168] MATERIAL "+name+" = "+entry.getValue());
                    }
                    Object entityIds=call(instance,"getEntityIds");
                    Object shadow=gameLoader.loadClass("net.irisshaders.iris.shaderpack.materialmap.NamespacedId")
                        .getConstructor(String.class,String.class).newInstance("minecraft","entity_shadow");
                    Method getInt=entityIds.getClass().getMethod("getInt",Object.class); getInt.setAccessible(true);
                    System.out.println("[STRATUS_QA168] ENTITY_SHADOW_ID "+getInt.invoke(entityIds,shadow));
                }
                case "QUIT" -> {
                    System.out.println("[STRATUS_QA168] GRACEFUL_QUIT");
                    call(client,"method_1592");
                }
                case "DONE" -> Files.writeString(game.resolve("qa-complete.txt"),argument+"\n");
                default -> throw new IllegalArgumentException(row);
            }
        } catch (Throwable error) { System.out.println("[STRATUS_QA168] ERROR " + error); error.printStackTrace(); }
    }
}
