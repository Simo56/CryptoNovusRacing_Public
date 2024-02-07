import bpy


obj = bpy.data.collections["Car"].objects["Carrozzeria"]

# Clear all nodes in a mat
def clear_material( material ):
    if material.node_tree:
        material.node_tree.links.clear()
        material.node_tree.nodes.clear()

materialToDelete = bpy.data.materials.get("Current")
# We clear it as we'll define it completely
clear_material( materialToDelete )

obj.data.materials.clear()

obj.data.materials.append(bpy.data.materials.get("Current"))
mat = bpy.data.materials.get("Current")
mat.use_nodes = True

bsdf = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")

texImage = mat.node_tree.nodes.new("ShaderNodeTexImage")
texImage.image = bpy.data.images.load("C:/Users/500/Desktop/Auto/CarLivree/Livery1.png",check_existing=True)
mat.node_tree.links.new(bsdf.inputs["Base Color"], texImage.outputs["Color"])

output = mat.node_tree.nodes.new("ShaderNodeOutputMaterial")
mat.node_tree.links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
