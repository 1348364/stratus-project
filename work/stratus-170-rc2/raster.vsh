#version 330 core
uniform int probeMaterial;uniform vec3 probeNormal;
out vec4 tintAndOpacity;out vec2 atlasCoordinate;out vec2 illuminationCoordinate;out vec3 relativeLocation;out vec3 orientedNormal;flat out int blockCategory;
void main(){vec2 q=vec2((gl_VertexID<<1)&2,gl_VertexID&2);gl_Position=vec4(q*2.-1.,0,1);tintAndOpacity=vec4(1);atlasCoordinate=vec2(.5);illuminationCoordinate=vec2(.95);relativeLocation=vec3(0,0,-3);orientedNormal=probeNormal;blockCategory=probeMaterial;}
