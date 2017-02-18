//Transformation Matrices
uniform mat4 HProjectionMatrix;
uniform mat4 HModelViewMatrix;

#if __VERSION__ >= 130

//Vertex position attribute
in vec2 HVertexPos2D;

//Multicolor attribute
in vec3 HMultiColor;
out vec4 multiColor;

#else

//Vertex position attribute
attribute vec2 HVertexPos2D;

//Multicolor attribute
attribute vec3 HMultiColor;
varying vec4 multiColor;

#endif

void main()
{
	//Process color
	multiColor = vec4( HMultiColor.r, HMultiColor.g, HMultiColor.b, 1.0 );
	
	//Process vertex
	gl_Position = HProjectionMatrix * HModelViewMatrix * vec4( HVertexPos2D.x, HVertexPos2D.y, 0.0, 1.0 );
}