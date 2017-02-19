#version 120

//Transformation Matrices
uniform mat4 HProjectionMatrix;
uniform mat4 HModelViewMatrix;

void main()
{
	//Process vertex
	gl_Position = HProjectionMatrix * HModelViewMatrix * gl_Vertex;
}