def construct_path_from_node(node):
    path = []
    cur_node = node
    while cur_node != None:
        path.append(cur_node)
        cur_node = cur_node.parent
    return path