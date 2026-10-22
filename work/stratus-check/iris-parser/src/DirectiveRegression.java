import java.nio.file.*;
import java.util.*;
import org.joml.Vector4f;
import net.irisshaders.iris.shaderpack.parsing.ConstDirectiveParser;
import net.irisshaders.iris.shaderpack.parsing.DispatchingDirectiveHolder;

public class DirectiveRegression {
    public static void main(String[] args) throws Exception {
        var parser = new DispatchingDirectiveHolder();
        var received = new HashMap<String, Vector4f>();
        var formats = new HashMap<String, String>();
        for (int i = 0; i < 3; i++) {
            String key = "colortex" + i + "ClearColor";
            parser.acceptConstVec4Directive(key, vector -> received.put(key, vector));
        }
        for (int i = 0; i < 5; i++) {
            String key = "colortex" + i + "Format";
            parser.acceptConstStringDirective(key, name -> formats.put(key, name));
        }
        boolean reproduced = false;
        var oldDirective = ConstDirectiveParser.findDirectiveInLine(
            "const vec4 colortex0ClearColor = vec4(0.0);").orElseThrow();
        try {
            parser.processDirective(oldDirective);
        } catch (ArrayIndexOutOfBoundsException expected) {
            reproduced = true;
            System.out.println("REPRODUCED installed Iris 1.10.8 parser failure: " + expected.getMessage());
        }
        if (!reproduced) throw new AssertionError("Regression fixture did not reproduce the reported error");
        for (var directive : ConstDirectiveParser.findDirectives(Files.readString(Path.of(args[0]))))
            parser.processDirective(directive);
        if (received.size() != 3) throw new AssertionError("Missing clear-colour directives: " + received.keySet());
        for (var item : received.entrySet()) {
            var v = item.getValue();
            if (v.x != 0 || v.y != 0 || v.z != 0 || v.w != 0)
                throw new AssertionError("Wrong clear colour: " + item);
        }
        if (formats.size() != 5) throw new AssertionError("Missing format directives: " + formats);
        for (int i = 0; i < 5; i++) {
            String expected = i == 0 || i == 2 ? "RGBA8" : "RGBA16F";
            if (!expected.equals(formats.get("colortex" + i + "Format")))
                throw new AssertionError("Iris lost symbolic texture format: " + formats);
        }
        System.out.println("PASS: all 5 texture-format directives retain the symbolic names expected by Iris");
        System.out.println("PASS: all 3 repaired clear colours accepted by the installed Iris parser bytecode");
        System.out.println("Only Iris/IrisLogging are isolated logger stubs; parser implementations are unmodified installed classes.");
    }
}
