#version 120

void main()
{
	//Process vertex
	gl_Position = gl_ProjectionMatrix * gl_ModelViewMatrix * gl_Vertex;
}