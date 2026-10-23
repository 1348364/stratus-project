import java.lang.instrument.Instrumentation;
import java.io.File;
import java.lang.reflect.*;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.function.Consumer;

/** Test-only Minecraft API driver. Installed solely in the isolated copied world. */
public final class Live1611Agent {
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
        new Live1611Agent().onInitializeClient();
    }

    private final Path actualGame = Path.of(System.getProperty("user.dir")).toAbsolutePath();
    private final Path game = work;
    private final Queue<String> actions = new ArrayDeque<>();
    private long resumeAt = 0;
    private Object client;
    private boolean initialized;
    private volatile boolean awaitingCommand;
    private double[] expectedCamera;
    private Object benchLogger; private Field benchStart,benchSize,benchData;
    private String gateTag;private long gateDeadline,gateStableAt,nextChunkPoll,lastReadyAt;private String lastChunkState="";private int gateLoaded,gateSections;private boolean benchChunksInvalid;private int benchChunkPolls;private double[] benchCamera;
    private int chunkInt(String json,String key){java.util.regex.Matcher m=java.util.regex.Pattern.compile("\""+key+"\":([0-9]+)").matcher(json);if(!m.find())throw new IllegalArgumentException(json);return Integer.parseInt(m.group(1));}
    private double[] currentCamera()throws Exception{Object p=client.getClass().getField("field_1724").get(client);return new double[]{(Double)call(p,"method_23317"),(Double)call(p,"method_23318"),(Double)call(p,"method_23321"),((Number)call(p,"method_36454")).doubleValue(),((Number)call(p,"method_36455")).doubleValue()};}
    private void pollReadiness()throws Exception{gateTag=null;}
    private String benchTag;private int cursor;private long benchEnd;
    private final ArrayList<Long> samples=new ArrayList<>();private int focusPolls,blurPolls;
    private int width,height;private boolean sizeChanged;
    private int[] dimensions()throws Exception{
        Class<?> glfw=gameLoader.loadClass("org.lwjgl.glfw.GLFW");long handle=(Long)call(call(client,"method_22683"),"method_4490");
        int[] w={0},h={0};glfw.getMethod("glfwGetFramebufferSize",long.class,int[].class,int[].class).invoke(null,handle,w,h);
        int focus=(Integer)glfw.getMethod("glfwGetWindowAttrib",long.class,int.class).invoke(null,handle,0x00020001);
        return new int[]{w[0],h[0],focus};
    }
    private void startBench(String argument)throws Exception{
        String[] args=argument.split(" ");benchTag=args[0];int[] dims=dimensions();width=dims[0];height=dims[1];sizeChanged=false;
        samples.clear();focusPolls=blurPolls=0;benchChunksInvalid=false;benchChunkPolls=0;benchCamera=currentCamera();nextChunkPoll=0;
        Object debug=call(client,"method_53526");Field logger=debug.getClass().getDeclaredField("field_45992");logger.setAccessible(true);benchLogger=logger.get(debug);
        benchStart=benchLogger.getClass().getDeclaredField("field_48815");benchStart.setAccessible(true);benchSize=benchLogger.getClass().getDeclaredField("field_48816");benchSize.setAccessible(true);benchData=benchLogger.getClass().getDeclaredField("field_48814");benchData.setAccessible(true);
        cursor=(benchStart.getInt(benchLogger)+benchSize.getInt(benchLogger))%240;
        benchEnd=System.nanoTime()+Long.parseLong(args[1])*1000000000L;
        Files.createDirectories(game.resolve("benchmarks"));
        if(dims[2]!=1||System.currentTimeMillis()-lastReadyAt>5000){Files.writeString(game.resolve("benchmarks/"+benchTag+".json"),"{\"valid_focused_sample\":false,\"reason\":\"Minecraft unfocused or no recent stable chunk gate; no FPS accepted\"}\n");benchTag=null;}
    }
    private void sampleBench()throws Exception{
        if(benchTag==null)return;
        int[] dims=dimensions();if(dims[2]==1)focusPolls++;else blurPolls++;sizeChanged|=dims[0]!=width||dims[1]!=height;
        int end=(benchStart.getInt(benchLogger)+benchSize.getInt(benchLogger))%240;
        long[][] buffer=(long[][])benchData.get(benchLogger);
        while(cursor!=end){long value=buffer[cursor][0];if(value>0)samples.add(value);cursor=(cursor+1)%240;}
        if(System.nanoTime()<benchEnd)return;
        double[] times=samples.stream().mapToDouble(v->v/1000000.0).sorted().toArray();double total=0;for(double v:times)total+=v;
        boolean valid=blurPolls==0&&!sizeChanged&&times.length>=10;boolean steady=valid&&!benchChunksInvalid&&benchChunkPolls>=10;
        String json=String.format(java.util.Locale.ROOT,"{\"valid_focused_sample\":%s,\"frames\":%d,\"average_fps\":%.4f,\"median_frame_ms\":%.4f,\"p95_frame_ms\":%.4f,\"p99_frame_ms\":%.4f,\"focused_polls\":%d,\"unfocused_polls\":%d,\"framebuffer\":[%d,%d],\"method\":\"Minecraft's frame-end duration ring; focus and size checked every 50ms main-thread poll\",\"raw_frame_ns\":%s}\n",valid,times.length,times.length*1000.0/Math.max(total,.0001),times.length>0?times[times.length/2]:0,times.length>0?times[(int)((times.length-1)*.95)]:0,times.length>0?times[(int)((times.length-1)*.99)]:0,focusPolls,blurPolls,width,height,samples.toString());
        json=json.substring(0,json.lastIndexOf('}'))+",\"valid_steady_state\":"+steady+",\"chunk_readiness_polls\":"+benchChunkPolls+",\"chunk_or_camera_changed\":"+benchChunksInvalid+",\"start_chunk_state\":"+lastChunkState+"}\n";
        Files.writeString(game.resolve("benchmarks/"+benchTag+".json"),json);benchTag=null;
    }

    public void onInitializeClient() {
        if (!actualGame.equals(Path.of(System.getProperty("user.home"),"Library/Application Support/ModrinthApp/profiles/Minecraft (1)")) || !game.toString().endsWith("work/stratus-refine-1611")) throw new IllegalStateException("QA helper requires explicit Main test launch");
        Thread worker = new Thread(() -> {
            while (!stopped) {
                try {
                    Thread.sleep(50);
                    client = gameLoader.loadClass("net.minecraft.class_310").getMethod("method_1551").invoke(null);
                    ((Executor)client).execute(this::poll);
                } catch (Throwable error) { System.out.println("[STRATUS_QA1611] WAIT " + error); }
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
        System.out.println("[STRATUS_QA1611] VERIFIED_PIPELINE "+pipeline.getClass().getName());
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
                System.out.println("[STRATUS_QA1611] READY: local world, HUD hidden");
            }
            Path request = game.resolve("qa-request.txt");
            if (Files.isRegularFile(request)) {
                for (String row : Files.readAllLines(request)) if (!row.isBlank() && !row.startsWith("#")) {
                    if(row.equals("CANCEL")){actions.clear();resumeAt=0;}else actions.add(row);
                }
                Files.move(request,game.resolve("qa-request-consumed.txt"),StandardCopyOption.REPLACE_EXISTING);
                System.out.println("[STRATUS_QA1611] QUEUED " + actions.size());
            }
            // Waits and screenshots must start after the integrated server has
            // actually executed a command, rather than after it was enqueued.
            pollReadiness();sampleBench();
            if (gateTag!=null || benchTag!=null || awaitingCommand || System.currentTimeMillis() < resumeAt || actions.isEmpty()) return;
            String row = actions.remove();
            String[] parts = row.split(" ", 2);
            String op = parts[0], argument = parts.length > 1 ? parts[1] : "";
            switch (op) {
                case "READY" -> {String[] a=argument.split(" ");gateTag=a[0];gateDeadline=System.currentTimeMillis()+Long.parseLong(a[1])*1000;gateStableAt=0;lastReadyAt=0;nextChunkPoll=0;}
                case "BENCH" -> startBench(argument);
                case "WAIT" -> resumeAt = System.currentTimeMillis() + Long.parseLong(argument) * 1000;
                case "CMD" -> {
                    awaitingCommand = true;
                    ((Executor)server).execute(() -> {
                    try {
                        Object manager = call(server, "method_3734"), source = call(server, "method_3739");
                        call(manager, "method_44252", source, argument);
                        System.out.println("[STRATUS_QA1611] COMMAND " + argument);
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
                            System.out.println("[STRATUS_QA1611] CAMERA "+coordinates+" creative-flight server confirmed");
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
                        System.out.println("[STRATUS_QA1611] VERIFIED_CAMERA "+Arrays.toString(actual));
                    }
                    Object framebuffer = call(client, "method_1522");
                    Method save = gameLoader.loadClass("net.minecraft.class_318").getMethod("method_22690", File.class,String.class,
                            gameLoader.loadClass("net.minecraft.class_276"),int.class,Consumer.class);
                    awaitingCommand=true;
                    save.invoke(null,game.toFile(),argument+".png",framebuffer,1,(Consumer<Object>)text -> {
                        System.out.println("[STRATUS_QA1611] SCREENSHOT " + argument + " " + text);
                        resumeAt=System.currentTimeMillis()+1500;awaitingCommand=false;
                    });
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
                    System.out.println("[STRATUS_QA1611] CREATIVE_FLIGHT_ENABLED");
                }
                case "HUD" -> {
                    Object options = client.getClass().getField("field_1690").get(client);
                    options.getClass().getField("field_1842").setBoolean(options, !argument.equals("show"));
                    System.out.println("[STRATUS_QA1611] HUD " + argument);
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
                    System.out.println("[STRATUS_QA1611] PACK " + argument);
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
                    System.out.println("[STRATUS_QA1611] MENU "+created.getClass().getName());
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
                    System.out.println("[STRATUS_QA1611] OPTIONS "+argument);
                }
                case "WIDGET" -> {
                    Object current=client.getClass().getField("field_1755").get(client);
                    List<?> children=(List<?>)call(current,"method_25396");
                    boolean found=false;
                    for(Object child:children){
                        try{
                            String label=(String)call(call(child,"method_25369"),"getString");
                            System.out.println("[STRATUS_QA1611] WIDGET "+child.getClass().getName()+" "+label);
                            if(label.equals(argument)){call(child,"method_25306",new Object[]{null});found=true;break;}
                        }catch(NoSuchMethodException ignored){}
                    }
                    if(!found)System.out.println("[STRATUS_QA1611] WIDGET_NOT_FOUND "+argument);
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
                                System.out.println("[STRATUS_QA1611] BUFFER "+i+" "+call(target,"getInternalFormat"));
                            }
                        }
                    }
                    Class<?> settings=gameLoader.loadClass("net.irisshaders.iris.shaderpack.materialmap.WorldRenderingSettings");
                    Object instance=settings.getField("INSTANCE").get(null);
                    Map<?,?> ids=(Map<?,?>)call(instance,"getBlockStateIds");
                    for(var entry:ids.entrySet()) {
                        String name=entry.getKey().toString();
                        if(name.startsWith("Block{minecraft:water}") || name.equals("Block{minecraft:stone}") || name.startsWith("Block{minecraft:iron_ore}") || name.startsWith("Block{minecraft:deepslate_iron_ore}"))
                            System.out.println("[STRATUS_QA1611] MATERIAL "+name+" = "+entry.getValue());
                    }
                    Object entityIds=call(instance,"getEntityIds");
                    Object shadow=gameLoader.loadClass("net.irisshaders.iris.shaderpack.materialmap.NamespacedId")
                        .getConstructor(String.class,String.class).newInstance("minecraft","entity_shadow");
                    Method getInt=entityIds.getClass().getMethod("getInt",Object.class); getInt.setAccessible(true);
                    System.out.println("[STRATUS_QA1611] ENTITY_SHADOW_ID "+getInt.invoke(entityIds,shadow));
                }
                case "QUIT" -> {
                    System.out.println("[STRATUS_QA1611] GRACEFUL_QUIT");
                    call(client,"method_1592");
                }
                case "DONE" -> Files.writeString(game.resolve("qa-complete.txt"),argument+"\n");
                default -> throw new IllegalArgumentException(row);
            }
        } catch (Throwable error) { System.out.println("[STRATUS_QA1611] ERROR " + error); error.printStackTrace(); }
    }
}
