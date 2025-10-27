precision mediump float;

attribute vec3 a_position;
attribute vec3 a_normal;


uniform vec4 u_lightPosition;
uniform vec4 u_lightColor;


uniform vec4 u_materialAmbient;
uniform vec4 u_materialDiffuse;
uniform vec4 u_materialSpecular;
uniform float u_materialShininess;

// Fog uniforms
uniform float u_startFog;
uniform float u_endFog;
uniform vec4 u_fogColor;

// Variables from vertex shader
varying vec3 v_worldPosition;
varying vec3 v_normal;
varying vec3 v_eyePosition;

// Variable for fog
varying float v_eyeDistance;

void main()
{
    // Ambient
    vec4 ambient = u_materialAmbient;
    
    // Diffuse
    vec3 lightDirection = normalize(u_lightPosition.xyz - v_worldPosition);
    float diffuseFactor = max(dot(v_normal, lightDirection), 0.0);
    vec4 diffuse = u_materialDiffuse * u_lightColor * diffuseFactor;
    
    // Specular
    vec3 viewDirection = normalize(-v_eyePosition);
    vec3 reflectionDirection = normalize(2.0 * dot(v_normal, lightDirection) * v_normal - lightDirection);
    float specularFactor = pow(max(dot(viewDirection, reflectionDirection), 0.0), u_materialShininess);
    vec4 specular = u_materialSpecular * u_lightColor * specularFactor;
    
    // Combine all lighting components
    vec4 finalColor = ambient + diffuse + specular;
    
    // Fog factor
    float fogFactor = (v_eyeDistance - u_startFog) / (u_endFog - u_startFog);
    fogFactor = max(0.0, min(1.0, fogFactor));
    
    // Mix fragment color with fog color based on distance
    gl_FragColor = mix(finalColor, u_fogColor, fogFactor);
}


