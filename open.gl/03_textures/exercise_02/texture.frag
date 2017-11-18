#version 330 core
in vec3 ourColor;
in vec2 TexCoord;

out vec4 color;

// Texture samplers
uniform sampler2D ourTexture1;
uniform sampler2D ourTexture2;
uniform float time;

void main()
{
    // Linearly interpolate between both textures (second texture is only slightly combined)
    // color = mix(texture(ourTexture1, TexCoord), texture(ourTexture2, TexCoord), 0.5);
    if (TexCoord.y > 0.5)
        color = texture(ourTexture1, TexCoord);
    else
        color = texture(ourTexture1, vec2(TexCoord.x+sin(TexCoord.y*60.0+time*2.0)/30.0, 1.0 - TexCoord.y)) * vec4(0.7, 0.7, 1.0, 1.0);
}