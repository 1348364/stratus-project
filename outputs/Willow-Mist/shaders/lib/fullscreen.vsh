out vec2 screenUV;
void main() {
    gl_Position = ftransform();
    screenUV = gl_MultiTexCoord0.xy;
}
