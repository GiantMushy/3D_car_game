attribute vec3 a_position;
attribute vec3 a_normal;

uniform mat4 u_model_matrix;
uniform mat4 u_projection_view_matrix;
uniform vec4 u_color;

// Point light uniforms (4 stadium lights)
uniform vec3 u_light_positions[4];
uniform vec3 u_light_colors[4];
uniform float u_light_intensities[4];

// NEW: Material properties
uniform vec3 u_camera_position;
uniform float u_shininess;      
uniform float u_specular_strength;  // How reflective the material is

varying vec4 v_color;

void main(void)
{
    vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
    vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);

    // Transform position and normal to world space
    position = u_model_matrix * position;
    normal = u_model_matrix * normal;
    
    vec3 world_pos = position.xyz;
    vec3 world_normal = normalize(normal.xyz);
    
    // Calculate lighting from all 4 stadium lights
    vec3 total_lighting = vec3(0.0, 0.0, 0.0);
    
    for(int i = 0; i < 4; i++) {
        vec3 light_dir = u_light_positions[i] - world_pos;
        float distance = length(light_dir);
        light_dir = normalize(light_dir);
        
        // Attenuation (inverse square law with minimum)
        float attenuation = u_light_intensities[i] / (1.0 + 0.001 * distance * distance);
        attenuation = max(attenuation, 0.0);
        
        // Lambertian diffuse lighting
        float diffuse = max(dot(world_normal, light_dir), 0.0);
        
        // Specular reflection (only if material is specular)
        float specular = 0.0;
        if(u_specular_strength > 0.0) {
            vec3 view_dir = normalize(u_camera_position - world_pos);
            vec3 reflect_dir = reflect(-light_dir, world_normal);
            specular = pow(max(dot(view_dir, reflect_dir), 0.0), u_shininess) * u_specular_strength;
        }
        
        total_lighting += u_light_colors[i] * (diffuse + specular) * attenuation;
    }
    
    // Very small ambient light so things aren't completely black
    vec3 ambient = vec3(0.01, 0.01, 0.015);
    total_lighting += ambient;
    
    // Clamp to prevent over-bright colors
    total_lighting = min(total_lighting, vec3(1.0, 1.0, 1.0));
    
    v_color = vec4(total_lighting * u_color.rgb, u_color.a);

    position = u_projection_view_matrix * position;
    gl_Position = position;
}