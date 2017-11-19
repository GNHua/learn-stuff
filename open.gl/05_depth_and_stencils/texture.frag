#version 330 core
in vec3 Color;
in vec2 Texcoord;

out vec4 outColor;

// Texture samplers
uniform sampler2D texKitten;
uniform sampler2D texPuppy;

void main()
{
    // Linearly interpolate between both textures (second texture is only slightly combined)
    outColor = vec4(Color, 1.0) * mix(texture(texKitten, Texcoord), texture(texPuppy, Texcoord), 0.5);;
}