import hou

# ref to current node we're in (subnetwork), get assets parm and evaluate
num_assets = hou.pwd().parm('assets').eval()
print(num_assets)

main_root_path = hou.pwd().parent().path()

# Main subnet
subnet = hou.node(main_root_path).createNode('subnet', 'instancer')
root_path = subnet.path()

# Move target to subnet
target_object_merge = hou.node(root_path).createNode('object_merge')
target_object_merge.parm('xformtype').set(1) # dropdown to 'transform into specified obj'
target_object_merge.parm('objpath1').set(hou.pwd().parm('target').eval()) # the path to the target aka /obj/geo1/grid1 

# Merge node
merge_node = hou.node(root_path).createNode('merge')

# Target node - grid
# target_node = hou.node(hou.pwd().parm('target').eval())
# Target node is now target_object_merge
# The scatter node below has to go into the subnet

# Scatter node so we can add points
scatter_node = target_object_merge.createOutputNode('scatter')
scatter_node.parm('relaxpoints').set(0)

# Attribute randomize
attr_randomize_names = scatter_node.createOutputNode('attribrandomize')
attr_randomize_names.parm('name').set('name')
attr_randomize_names.parm('distribution').set('discrete')
attr_randomize_names.parm('valuetype').set(1) # from float to string
attr_randomize_names.parm('values').set(num_assets)

for i in range(num_assets):
    prim_name = hou.pwd().parm('asset{}'.format(i+1)).eval().split('/')[-1]
    node = hou.node(root_path).createNode('object_merge', prim_name)
    node.parm('xformtype').set(1) # dropdown to 'transform into specified obj'
    node.parm('objpath1').set(hou.pwd().parm('asset{}'.format(i+1)).eval()) # the path to the target aka /obj/geo1/grid1 
    
    pack_node = node.createOutputNode('pack')
    name_node = pack_node.createOutputNode('name')
    name_node.parm('name1').set(node.name())
    
    merge_node.setNextInput(name_node)
    
    attr_randomize_names.parm('strvalue{}'.format(i)).set(node.name())
    
    node.moveToGoodPosition()
    
merge_node.moveToGoodPosition()

# x will give a value (0, 1, etc.) and node will give a node
# for x, node in enumerate(nodes):
    
# Now copy to points
copy_node = hou.node(root_path).createNode('copytopoints::2.0')
copy_node.parm('useidattrib').set(1) # toggle - set to 1 to turn on
copy_node.parm('idattrib').set('name')
copy_node.setInput(0, merge_node)
copy_node.setInput(1, attr_randomize_names)
copy_node.moveToGoodPosition()
