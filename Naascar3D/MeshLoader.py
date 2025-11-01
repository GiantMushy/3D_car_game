import json
import os
from typing import Dict, List, Optional, Tuple
from ObjLoader import ObjLoader

class MeshData:
    def __init__(self, positions: List[float], normals: List[float], indices: List[int]):
        self.positions = positions
        self.normals = normals
        self.indices = indices

class MeshLoader:
    def __init__(self, mesh_directory="meshes"):
        self.mesh_directory = mesh_directory
        self.ensure_directory_exists()
    
    def ensure_directory_exists(self):
        if not os.path.exists(self.mesh_directory):
            os.makedirs(self.mesh_directory)
    
    def save_mesh(self, name: str, positions: List[float], normals: List[float], indices: Optional[List[int]] = None):
        """Save mesh data to a JSON file"""
        mesh_data = {
            "positions": positions,
            "normals": normals, 
            "indices": indices
        }
        
        filepath = os.path.join(self.mesh_directory, f"{name}.json")
        with open(filepath, 'w') as f:
            json.dump(mesh_data, f, indent=2)
        
        print(f"Saved mesh: {filepath}")
    
    def load_mesh(self, name: str) -> MeshData:
        """Load mesh data from a JSON file"""
        filepath = os.path.join(self.mesh_directory, f"{name}.json")
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Mesh file not found: {filepath}")
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        return MeshData(
            positions=data["positions"],
            normals=data["normals"], 
            indices=data.get("indices")
        )
    
    def load_obj_and_cache(self, obj_filepath: str, cache_name: str) -> MeshData:
        """Load OBJ file and cache it as JSON for faster future loading"""
        if self.mesh_exists(cache_name):
            return self.load_mesh(cache_name)
        
        # Load from OBJ and cache
        positions, normals, indices = ObjLoader.load_obj(obj_filepath)
        self.save_mesh(cache_name, positions, normals, indices)
        
        return MeshData(positions, normals, indices)
    
    def mesh_exists(self, name: str) -> bool:
        """Check if a mesh file exists"""
        filepath = os.path.join(self.mesh_directory, f"{name}.json")
        return os.path.exists(filepath)