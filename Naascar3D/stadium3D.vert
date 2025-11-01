attribute vec3 a_position;
attribute vec3 a_normal;

uniform mat4 u_model_matrix;
uniform mat4 u_projection_view_matrix;
uniform vec4 u_color;

// Pass to fragment shader
varying vec3 v_world_pos;
varying vec3 v_world_normal;
varying vec4 v_base_color;

void main(void)
{
    vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
    vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);

    // Transform position and normal to world space
    position = u_model_matrix * position;
    normal = u_model_matrix * normal;
    
    // Pass world space data to fragment shader
    v_world_pos = position.xyz;
    v_world_normal = normalize(normal.xyz);  // Use the transformed normal
    v_base_color = u_color;

    // Transform to clip space
    position = u_projection_view_matrix * position;
    gl_Position = position;
}