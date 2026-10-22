package qa.mixin;
import qa.FrameBench;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
@Mixin(targets="net.minecraft.class_310")
public abstract class StratusFrameMixin {
    @Inject(method="method_1523(Z)V",at=@At("HEAD"),remap=false)
    private void stratusFrame(boolean tick,CallbackInfo ci){FrameBench.frame();}
}
