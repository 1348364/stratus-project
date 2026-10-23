out vec2 rasterUV;
void main() {
    rasterUV = gl_MultiTexCoord0.st;
    gl_Position = vec4(rasterUV * 2.0 - 1.0, 0.0, 1.0);
}
