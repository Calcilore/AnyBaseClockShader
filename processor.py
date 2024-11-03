import os
import re

# Specify the directory where your .frag files are located
src_path = './src'
out_path = './target'

os.makedirs(out_path, exist_ok=True)

# List of variables to update
variables_to_update = [
    'iTime', 'iTimeDelta', 'iFrameRate', 'iSampleRate', 
    'iFrame', 'iDate', 'iMouse', 'iResolution', 
    r'iChannelTime', r'iChannelResolution'
]

# Header and footer to append
header = '''#version 450

layout(location = 0) in vec2 qt_TexCoord0;
layout(location = 0) out vec4 fragColor;

layout(std140, binding = 0) uniform buf { 
    mat4 qt_Matrix;
    float qt_Opacity;
    float iTime;
    float iTimeDelta;
    float iFrameRate;
    float iSampleRate;
    int iFrame;
    vec4 iDate;
    vec4 iMouse;
    vec3 iResolution;
    float iChannelTime[4];
    vec3 iChannelResolution[4];
} ubuf;

layout(binding = 1) uniform sampler2D iChannel0;
layout(binding = 1) uniform sampler2D iChannel1;
layout(binding = 1) uniform sampler2D iChannel2;
layout(binding = 1) uniform sampler2D iChannel3;

vec2 fragCoord = vec2(qt_TexCoord0.x, 1.0 - qt_TexCoord0.y) * ubuf.iResolution.xy;

'''

footer = '''

void main() {
    vec4 color = vec4(0.0);
    mainImage(color, fragCoord);
    fragColor = color;
}
'''

for root, dirs, files in os.walk(src_path):
    for file in files:
        if file.endswith('.frag'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Update variable instances
                for var in variables_to_update:
                    content = re.sub(r'\b' + var + r'\b', 'ubuf.' + var, content)
                
                content = header + content + footer
                
                # Write the updated content back to the file
                with open(os.path.join(out_path, file), "w", encoding='utf-8') as w:
                    w.write(content)
