attribute vec3 a_position;
attribute vec3 a_normal;

uniform mat4 u_modelMatrix;
uniform mat4 u_viewMatrix;
uniform mat4 u_projectionMatrix;
uniform mat4 u_normalMatrix;

uniform vec4 u_lightPosition;
uniform vec4 u_lightColor;


uniform vec4 u_materialAmbient;
uniform vec4 u_materialDiffuse;
uniform vec4 u_materialSpecular;
uniform float u_materialShininess;

uniform float u_startFog;
uniform float u_endFog;

// Varying variables for lighting calculations
varying vec3 v_worldPosition;
varying vec3 v_normal;
varying vec3 v_eyePosition;

// Varying variable for fog
varying float v_eyeDistance;

void main()
{
    // Transform position to world coordinates
    vec4 worldPosition = u_modelMatrix * vec4(a_position, 1.0);
    v_worldPosition = worldPosition.xyz;
    
    // Transform position to eye coordinates
    vec4 eyePosition = u_viewMatrix * worldPosition;
    v_eyePosition = eyePosition.xyz;
    
    // Transform position to clip coordinates and set gl_Position
    gl_Position = u_projectionMatrix * eyePosition;
    
    // Transform normal to world space for lighting
    v_normal = normalize((u_normalMatrix * vec4(a_normal, 0.0)).xyz);
    
    // Calculate distance from camera for fog
    v_eyeDistance = length(eyePosition);
}

