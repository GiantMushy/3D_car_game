import os
from typing import List, Tuple

class ObjLoader:
    @staticmethod
    def load_obj(filepath: str) -> Tuple[List[float], List[float], List[int]]:
        """Load OBJ file and return positions, normals, and indices"""
        vertices = []
        normals = []
        faces = []
        
        position_array = []
        normal_array = []
        index_array = []
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"OBJ file not found: {filepath}")
        
        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split()
                if not parts:
                    continue
                
                if parts[0] == 'v':  # Vertex position
                    # Skip the color values if present (the 1 1 1 at the end)
                    x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                    vertices.append((x, y, z))
                
                elif parts[0] == 'vn':  # Vertex normal
                    x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                    normals.append((x, y, z))
                
                elif parts[0] == 'f':  # Face
                    face_vertices = []
                    face_normals = []
                    
                    for vertex_data in parts[1:]:
                        # Handle format: vertex/texture/normal or vertex//normal
                        indices = vertex_data.split('/')
                        vertex_idx = int(indices[0]) - 1  # OBJ uses 1-based indexing
                        
                        if len(indices) >= 3 and indices[2]:  # Has normal index
                            normal_idx = int(indices[2]) - 1
                        else:
                            normal_idx = vertex_idx  # Assume same index if not specified
                        
                        face_vertices.append(vertex_idx)
                        face_normals.append(normal_idx)
                    
                    faces.append((face_vertices, face_normals))
        
        # Convert to flat arrays for OpenGL
        vertex_index = 0
        for face_verts, face_norms in faces:
            # Triangulate faces (assuming they're already triangles or quads)
            if len(face_verts) == 3:  # Triangle
                triangles = [(0, 1, 2)]
            elif len(face_verts) == 4:  # Quad - split into two triangles
                triangles = [(0, 1, 2), (0, 2, 3)]
            else:
                # For polygons with more than 4 vertices, use fan triangulation
                triangles = [(0, i, i+1) for i in range(1, len(face_verts)-1)]
            
            for tri in triangles:
                for i in tri:
                    v_idx = face_verts[i]
                    n_idx = face_norms[i]
                    
                    # Add vertex position
                    if v_idx < len(vertices):
                        position_array.extend(vertices[v_idx])
                    else:
                        position_array.extend([0.0, 0.0, 0.0])
                    
                    # Add vertex normal
                    if n_idx < len(normals):
                        normal_array.extend(normals[n_idx])
                    else:
                        normal_array.extend([0.0, 1.0, 0.0])  # Default normal
                    
                    index_array.append(vertex_index)
                    vertex_index += 1
        
        return position_array, normal_array, index_array