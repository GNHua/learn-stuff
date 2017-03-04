#if __VERSION__ >= 130

//Multicolor attribute
in vec4 multiColor;

//Final color
out vec4 gl_FragColor;

#else

//Multicolor attribute
varying vec4 multiColor;

#endif

void main()
{
	//Set fragment
	gl_FragColor = multiColor;
}