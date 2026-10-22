import net.fabricmc.api.ClientModInitializer;
import java.io.File;
import java.lang.reflect.*;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.function.Consumer;

/** Test-only Minecraft API driver. Installed solely in the isolated copied world. */
public final class StratusVisualQA implements ClientModInitializer {
    private final Path game = Path.of(System.getProperty("user.dir"));
    private final Queue<String> actions = new ArrayDeque<>();
    private long resumeAt = 0;
    private Object client;
    private boolean initialized;
    private volatile boolean awaitingCommand;
    private double[] expectedCamera;

    public void onInitializeClient() {
        if (!game.toString().endsWith("work/minecraft-smoke")) throw new IllegalStateException("QA helper is test-directory only");
        Thread worker = new Thread(() -> {
            while (true) {
                try {
                    Thread.sleep(750);
                    client = Class.forName("net.minecraft.class_310").getMethod("method_1551").invoke(null);
                    ((Executor)client).execute(this::poll);
                } catch (Throwable error) { System.out.println("[STRATUS_QA] WAIT " + error); }
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
        Object manager=Class.forName("net.irisshaders.iris.Iris").getMethod("getPipelineManager").invoke(null);
        Object pipeline=call(manager,"getPipelineNullable");
        if(pipeline==null||!pipeline.getClass().getName().contains("IrisRenderingPipeline")){
            actions.clear();throw new IllegalStateException("Shader pipeline failed; capture queue stopped");
        }
        System.out.println("[STRATUS_QA] VERIFIED_PIPELINE "+pipeline.getClass().getName());
    }
    private void poll() {
        try {
            Object server = call(client, "method_1576");
            if (server == null || client.getClass().getField("field_1724").get(client) == null) return;
            if (!initialized) {
                Object options = client.getClass().getField("field_1690").get(client);
                options.getClass().getField("field_1842").setBoolean(options, true);
                options.getClass().getField("field_1837").setBoolean(options, false);
                call(client,"method_1507",new Object[]{null});
                initialized = true;
                System.out.println("[STRATUS_QA] READY: local world, HUD hidden");
            }
            Path request = game.resolve("qa-request.txt");
            if (Files.isRegularFile(request)) {
                for (String row : Files.readAllLines(request)) if (!row.isBlank() && !row.startsWith("#")) {
                    if(row.equals("CANCEL")){actions.clear();resumeAt=0;}else actions.add(row);
                }
                Files.move(request,game.resolve("qa-request-consumed.txt"),StandardCopyOption.REPLACE_EXISTING);
                System.out.println("[STRATUS_QA] QUEUED " + actions.size());
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
                        System.out.println("[STRATUS_QA] COMMAND " + argument);
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
                            call(manager,"method_44252",source,"tp ShaderCheck "+coordinates);
                            Object player=call(call(server,"method_3760"),"method_14566","ShaderCheck");
                            Object abilities=call(player,"method_31549");
                            abilities.getClass().getField("field_7479").setBoolean(abilities,true);
                            call(player,"method_7355");
                            System.out.println("[STRATUS_QA] CAMERA "+coordinates+" creative-flight server confirmed");
                        } catch(Throwable error){error.printStackTrace();}
                        finally{awaitingCommand=false;}
                    });
                }
                case "SHOT" -> {
                    if(!argument.contains("-menu-")&&client.getClass().getField("field_1755").get(client)!=null){
                        call(client,"method_1507",new Object[]{null});
                        ((ArrayDeque<String>)actions).addFirst(row);resumeAt=System.currentTimeMillis()+2500;return;
                    }
                    requireShader();
                    if(expectedCamera!=null){
                        Object player=client.getClass().getField("field_1724").get(client);
                        double[] actual={(Double)call(player,"method_23317"),(Double)call(player,"method_23318"),(Double)call(player,"method_23321")};
                        for(int i=0;i<3;i++)if(Math.abs(actual[i]-expectedCamera[i])>0.15){actions.clear();throw new IllegalStateException("Camera moved before capture: "+Arrays.toString(actual)+" expected "+Arrays.toString(expectedCamera));}
                        System.out.println("[STRATUS_QA] VERIFIED_CAMERA "+Arrays.toString(actual));
                    }
                    Object framebuffer = call(client, "method_1522");
                    Method save = Class.forName("net.minecraft.class_318").getMethod("method_22690", File.class,String.class,
                            Class.forName("net.minecraft.class_276"),int.class,Consumer.class);
                    save.invoke(null,game.toFile(),argument+".png",framebuffer,1,(Consumer<Object>)text ->
                            System.out.println("[STRATUS_QA] SCREENSHOT " + argument + " " + text));
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
                    System.out.println("[STRATUS_QA] CREATIVE_FLIGHT_ENABLED");
                }
                case "HUD" -> {
                    Object options = client.getClass().getField("field_1690").get(client);
                    options.getClass().getField("field_1842").setBoolean(options, !argument.equals("show"));
                    System.out.println("[STRATUS_QA] HUD " + argument);
                }
                case "PACK" -> {
                    Class<?> iris = Class.forName("net.irisshaders.iris.Iris");
                    Object config = iris.getMethod("getIrisConfig").invoke(null);
                    call(config,"setShaderPackName",argument); call(config,"setShadersEnabled",true);
                    call(config,"save");
                    iris.getMethod("reload").invoke(null);
                    requireShader();
                    System.out.println("[STRATUS_QA] PACK " + argument);
                    resumeAt = System.currentTimeMillis()+5000;
                }
                case "BENCH" -> {
                    String[] parameters=argument.split(" ");
                    Class<?> glfw=Class.forName("org.lwjgl.glfw.GLFW");
                    Object window=call(client,"method_22683");
                    long handle=(Long)call(window,"method_4490");
                    glfw.getMethod("glfwRestoreWindow",long.class).invoke(null,handle);
                    glfw.getMethod("glfwFocusWindow",long.class).invoke(null,handle);
                    qa.FrameBench.start(parameters[0],Integer.parseInt(parameters[1]));
                    resumeAt=System.currentTimeMillis()+(Integer.parseInt(parameters[1])+2)*1000L;
                }
                case "MENU" -> {
                    Class<?> screen=Class.forName("net.irisshaders.iris.gui.screen.ShaderPackScreen");
                    Object parent=client.getClass().getField("field_1755").get(client);
                    Object created=screen.getConstructors()[0].newInstance(parent);
                    call(client,"method_1507",created);
                    System.out.println("[STRATUS_QA] MENU "+created.getClass().getName());
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
                    System.out.println("[STRATUS_QA] OPTIONS "+argument);
                }
                case "WIDGET" -> {
                    Object current=client.getClass().getField("field_1755").get(client);
                    List<?> children=(List<?>)call(current,"method_25396");
                    boolean found=false;
                    for(Object child:children){
                        try{
                            String label=(String)call(call(child,"method_25369"),"getString");
                            System.out.println("[STRATUS_QA] WIDGET "+child.getClass().getName()+" "+label);
                            if(label.equals(argument)){call(child,"method_25306",new Object[]{null});found=true;break;}
                        }catch(NoSuchMethodException ignored){}
                    }
                    if(!found)System.out.println("[STRATUS_QA] WIDGET_NOT_FOUND "+argument);
                }
                case "STATE" -> {
                    Class<?> iris = Class.forName("net.irisshaders.iris.Iris");
                    Object manager = iris.getMethod("getPipelineManager").invoke(null);
                    Object pipeline = call(manager,"getPipelineNullable");
                    for (Field field : pipeline.getClass().getDeclaredFields()) {
                        if (field.getType().getName().equals("net.irisshaders.iris.targets.RenderTargets")) {
                            field.setAccessible(true); Object targets=field.get(pipeline);
                            for(int i=0;i<8;i++) {
                                Object target=call(targets,"get",i);
                                System.out.println("[STRATUS_QA] BUFFER "+i+" "+call(target,"getInternalFormat"));
                            }
                        }
                    }
                    Class<?> settings=Class.forName("net.irisshaders.iris.shaderpack.materialmap.WorldRenderingSettings");
                    Object instance=settings.getField("INSTANCE").get(null);
                    Map<?,?> ids=(Map<?,?>)call(instance,"getBlockStateIds");
                    for(var entry:ids.entrySet()) {
                        String name=entry.getKey().toString();
                        if(name.startsWith("Block{minecraft:water}") || name.equals("Block{minecraft:stone}") || name.startsWith("Block{minecraft:iron_ore}") || name.startsWith("Block{minecraft:deepslate_iron_ore}"))
                            System.out.println("[STRATUS_QA] MATERIAL "+name+" = "+entry.getValue());
                    }
                    Object entityIds=call(instance,"getEntityIds");
                    Object shadow=Class.forName("net.irisshaders.iris.shaderpack.materialmap.NamespacedId")
                        .getConstructor(String.class,String.class).newInstance("minecraft","entity_shadow");
                    Method getInt=entityIds.getClass().getMethod("getInt",Object.class); getInt.setAccessible(true);
                    System.out.println("[STRATUS_QA] ENTITY_SHADOW_ID "+getInt.invoke(entityIds,shadow));
                }
                case "QUIT" -> {
                    System.out.println("[STRATUS_QA] GRACEFUL_QUIT");
                    call(client,"method_1592");
                }
                case "DONE" -> Files.writeString(game.resolve("qa-complete.txt"),argument+"\n");
                default -> throw new IllegalArgumentException(row);
            }
        } catch (Throwable error) { System.out.println("[STRATUS_QA] ERROR " + error); error.printStackTrace(); }
    }
}
