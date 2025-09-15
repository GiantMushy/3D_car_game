attribute vec3 a_position;
//## ADD CODE HERE ##

uniform mat4 u_model_matrix;
uniform mat4 u_projection_view_matrix;

varying vec4 v_color;  //Leave the varying variables alone to begin with

void main(void)
{
	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
	//## ADD CODE HERE ##

	position = u_model_matrix * position;
	//## ADD CODE HERE ##

	float light_factor_1 = max(dot(normalize(normal), normalize(vec4(1, 2, 3, 0))), 0.0);
	float light_factor_2 = max(dot(normalize(normal), normalize(vec4(-3, -2, -1, 0))), 0.0);
	v_color = (light_factor_1 + light_factor_2) * vec4(1,1,1,1); // ### --- Change this vector (pure white) to color variable --- #####

	// ### --- Change the projection_view_matrix to separate view and projection matrices --- ### 
	position = u_projection_view_matrix * position;

	gl_Position = position;
}