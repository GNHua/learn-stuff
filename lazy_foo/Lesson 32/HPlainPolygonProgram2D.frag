#version 120

//Plain polygon color
uniform vec4 HPolygonColor = vec4( 1.0, 1.0, 1.0, 1.0 );

void main()
{
	//Set fragment
	gl_FragColor = HPolygonColor;
}
