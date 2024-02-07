import bpy
from bpy import context, data, ops

obj = bpy.data.collections["Car"].objects["Carrozzeria"]
obj.data.materials.append(bpy.data.materials.new(name="Current"))

for i in range(1,51):
    mat = bpy.data.materials.new(name="Livery"+str(i))
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    texImage = mat.node_tree.nodes.new("ShaderNodeTexImage")
    texImage.image = bpy.data.images.load("C:/Users/500/Desktop/Auto/CarLivree/Livery"+str(i)+".png")
    mat.node_tree.links.new(bsdf.inputs["Base Color"], texImage.outputs["Color"])
    #Assign it to object
    obj.data.materials.append(mat)
    print("Creato materiale per Livery"+str(i))
    #if obj.data.materials:
        #print("assegnato il primo")
        #obj.data.materials[0] = mat
    #else:
        #print("append")
        #obj.data.materials.append

#obj.data.materials[0] = bpy.data.materials.get("Livery36")
print("Finito!")
