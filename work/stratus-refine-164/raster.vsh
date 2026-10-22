#version 330 core
out vec4 tintAndOpacity;out vec2 atlasCoordinate;out vec2 illuminationCoordinate;
out vec3 relativeLocation;out vec3 orientedNormal;flat out int blockCategory;
uniform int fixtureCategory;
void main(){vec2 p=vec2((gl_VertexID<<1)&2,gl_VertexID&2);gl_Position=vec4(p*2.-1.,0,1);tintAndOpacity=vec4(1,1,1,.5);atlasCoordinate=vec2(.5);illuminationCoordinate=vec2(1.,31.)/32.;relativeLocation=vec3(0,0,-2);orientedNormal=vec3(0,-1,0);blockCategory=fixtureCategory;}
