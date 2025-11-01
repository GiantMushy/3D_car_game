precision mediump float;

// Point light uniforms (4 stadium lights + Underglow)
uniform vec3 u_light_positions[5];
uniform vec3 u_light_colors[5];
uniform float u_light_intensities[5];
uniform bool u_light_enabled[5];

// Material properties
uniform vec3 u_camera_position;
uniform float u_shininess;      
uniform float u_specular_strength;

// Directional Light uniforms (moonlight)
uniform vec3 u_directional_light_direction;
uniform vec3 u_directional_light_color;
uniform float u_directional_light_intensity;
uniform bool u_directional_light_enabled;

// From vertex shader
varying vec3 v_world_pos;
varying vec3 v_world_normal;
varying vec4 v_base_color;

void main(void)
{
    vec3 world_pos = v_world_pos;
    vec3 world_normal = normalize(v_world_normal);
    
    vec3 total_lighting = vec3(0.0, 0.0, 0.0);
    
    // ---- 1. DIRECTIONAL LIGHT (moonlight)
    if(u_directional_light_enabled) {
        vec3 light_dir = normalize(-u_directional_light_direction);
        float diffuse = max(dot(world_normal, light_dir), 0.0);
        
        float specular = 0.0;
        if(u_specular_strength > 0.0) {
            vec3 view_dir = normalize(u_camera_position - world_pos);
            vec3 reflect_dir = reflect(-light_dir, world_normal);
            specular = pow(max(dot(view_dir, reflect_dir), 0.0), u_shininess) * u_specular_strength;
        }
        
        total_lighting += u_directional_light_color * (diffuse + specular) * u_directional_light_intensity;
    }
    
    // ---- 2. POSITIONAL LIGHTS (4 stadium lights + underglow) - PER PIXEL!
    for(int i = 0; i < 5; i++) {
        if(!u_light_enabled[i]) continue;

        vec3 light_dir = u_light_positions[i] - world_pos;
        float distance = length(light_dir);
        light_dir = normalize(light_dir);
        
        // Different attenuation for underglow (index 4) vs stadium lights
        float attenuation;
        if(i == 4) {
            // Underglow: very strong close-range falloff
            attenuation = u_light_intensities[i] / (1.0 + 0.5 * distance + 2.0 * distance * distance);
        } else {
            // Stadium lights: gentler falloff
            attenuation = u_light_intensities[i] / (1.0 + 0.002 * distance * distance);
        }
        attenuation = max(attenuation, 0.0);
        
        float diffuse = max(dot(world_normal, light_dir), 0.0);
        
        float specular = 0.0;
        if(u_specular_strength > 0.0) {
            vec3 view_dir = normalize(u_camera_position - world_pos);
            vec3 reflect_dir = reflect(-light_dir, world_normal);
            specular = pow(max(dot(view_dir, reflect_dir), 0.0), u_shininess) * u_specular_strength;
        }
        
        total_lighting += u_light_colors[i] * (diffuse + specular) * attenuation;
    }
    
    // Small ambient light so things aren't completely black
    vec3 ambient = vec3(0.01, 0.01, 0.015);
    total_lighting += ambient;
    
    // Clamp to prevent over-bright colors
    total_lighting = min(total_lighting, vec3(1.0, 1.0, 1.0));
    
    gl_FragColor = vec4(total_lighting * v_base_color.rgb, v_base_color.a);
}