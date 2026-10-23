from pathlib import Path
w=Path('work/stratus-refine-1611');chunk=w/'agent/ChunkState1611.java';s=chunk.read_text();s=s.replace(' static String state(Object client,ClassLoader cl)throws Exception{',' static int cachedRequired,cachedPresent;\n static String state(Object client,ClassLoader cl)throws Exception{return state(client,cl,true);}\n static String state(Object client,ClassLoader cl,boolean scan)throws Exception{');old='  for(int x=-radius;x<=radius;x++)for(int z=-radius;z<=radius;z++)if(x*x+z*z<=radius*radius){required++;if(call(manager,"method_2857",cx+x,cz+z,full,false)!=null)present++;}';new='  if(scan){'+old.strip()+'cachedRequired=required;cachedPresent=present;}else{required=cachedRequired;present=cachedPresent;}';assert old in s;s=s.replace(old,new);chunk.write_text(s)
s=Path('work/stratus-refine-1610/agent/Live1610Agent.java').read_text().replace('Live1610Agent','Live1611Agent').replace('STRATUS_QA1610','STRATUS_QA1611').replace('work/stratus-refine-1610','work/stratus-refine-1611')
s=s.replace('    private String benchTag;', '''    private String gateTag;private long gateDeadline,gateStableAt,nextChunkPoll,lastReadyAt;private String lastChunkState="";private int gateLoaded,gateSections;private boolean benchChunksInvalid;private int benchChunkPolls;private double[] benchCamera;
    private int chunkInt(String json,String key){java.util.regex.Matcher m=java.util.regex.Pattern.compile("\\\""+key+"\\\":([0-9]+)").matcher(json);if(!m.find())throw new IllegalArgumentException(json);return Integer.parseInt(m.group(1));}
    private double[] currentCamera()throws Exception{Object p=client.getClass().getField("field_1724").get(client);return new double[]{(Double)call(p,"method_23317"),(Double)call(p,"method_23318"),(Double)call(p,"method_23321"),((Number)call(p,"method_36454")).doubleValue(),((Number)call(p,"method_36455")).doubleValue()};}
    private void pollReadiness()throws Exception{
      long now=System.currentTimeMillis();if((gateTag==null&&benchTag==null)||now<nextChunkPoll)return;nextChunkPoll=now+1000;
      String state=ChunkState1611.state(client,gameLoader,gateTag!=null);int loaded=chunkInt(state,"client_loaded_columns"),sections=chunkInt(state,"render_sections");boolean ready=state.contains("\\\"ready\\\":true");
      Files.writeString(game.resolve("chunk-readiness.jsonl"),"{\\\"time_ms\\\":"+now+",\\\"phase\\\":\\\""+(gateTag==null?benchTag:gateTag)+"\\\",\\\"sampling\\\":"+(benchTag!=null)+",\\\"state\\\":"+state+"}\\n",java.nio.file.StandardOpenOption.CREATE,java.nio.file.StandardOpenOption.APPEND);
      if(gateTag!=null){if(!ready||loaded!=gateLoaded||sections!=gateSections){gateStableAt=0;gateLoaded=loaded;gateSections=sections;}else if(gateStableAt==0)gateStableAt=now;
        if(ready&&gateStableAt>0&&now-gateStableAt>=5000){lastReadyAt=now;lastChunkState=state;Files.createDirectories(game.resolve("readiness"));Files.writeString(game.resolve("readiness/"+gateTag+".json"),"{\\\"stable_ms\\\":"+(now-gateStableAt)+",\\\"state\\\":"+state+"}\\n");System.out.println("[STRATUS_QA1611] CHUNKS_READY "+gateTag+" "+state);gateTag=null;}
        else if(now>gateDeadline){actions.clear();Files.writeString(game.resolve("readiness-failure.txt"),gateTag+" timeout "+state);gateTag=null;}
      }else{benchChunkPolls++;if(!ready||loaded!=gateLoaded||sections!=gateSections)benchChunksInvalid=true;double[] actual=currentCamera();for(int j=0;j<5;j++)if(Math.abs(actual[j]-benchCamera[j])>.001)benchChunksInvalid=true;}
    }
    private String benchTag;''')
s=s.replace('        samples.clear();focusPolls=blurPolls=0;', '        samples.clear();focusPolls=blurPolls=0;benchChunksInvalid=false;benchChunkPolls=0;benchCamera=currentCamera();nextChunkPoll=0;')
s=s.replace('        if(dims[2]!=1){', '        if(dims[2]!=1||System.currentTimeMillis()-lastReadyAt>5000){')
s=s.replace('Minecraft unfocused; no FPS accepted','Minecraft unfocused or no recent stable chunk gate; no FPS accepted')
s=s.replace('boolean valid=blurPolls==0&&!sizeChanged&&times.length>=10;', 'boolean valid=blurPolls==0&&!sizeChanged&&times.length>=10;boolean steady=valid&&!benchChunksInvalid&&benchChunkPolls>=10;')
s=s.replace('        Files.writeString(game.resolve("benchmarks/"+benchTag+".json"),json);benchTag=null;', '''        json=json.substring(0,json.lastIndexOf('}'))+",\\\"valid_steady_state\\\":"+steady+",\\\"chunk_readiness_polls\\\":"+benchChunkPolls+",\\\"chunk_or_camera_changed\\\":"+benchChunksInvalid+",\\\"start_chunk_state\\\":"+lastChunkState+"}\\n";
        Files.writeString(game.resolve("benchmarks/"+benchTag+".json"),json);benchTag=null;''')
s=s.replace('            sampleBench();', '            pollReadiness();sampleBench();')
s=s.replace('if (benchTag!=null || awaitingCommand', 'if (gateTag!=null || benchTag!=null || awaitingCommand')
s=s.replace('                case "BENCH" -> startBench(argument);', '''                case "READY" -> {String[] a=argument.split(" ");gateTag=a[0];gateDeadline=System.currentTimeMillis()+Long.parseLong(a[1])*1000;gateStableAt=0;lastReadyAt=0;nextChunkPoll=0;}
                case "BENCH" -> startBench(argument);''')
(w/'agent/Live1611Agent.java').write_text(s)
s=Path('work/stratus-refine-1610/agent/ActiveBenchmark1610.java').read_text().replace('ActiveBenchmark1610','ActiveBenchmark1611').replace('work/stratus-refine-1610','work/stratus-refine-1611');(w/'agent/ActiveBenchmark1611.java').write_text(s)
