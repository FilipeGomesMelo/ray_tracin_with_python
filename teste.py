object_list = []
vertices_list = []
for obj in object_list:
    if "triangle" in obj and obj["triangle"] not in vertices_list:
        vertices_list.append(obj["triangle"][0])
        vertices_list.append(obj["triangle"][1])
        vertices_list.append(obj["triangle"][2])

print(*vertices_list, sep=',\n')

triangle_list = []
for obj in object_list:
    if "triangle" in obj:
        triangle_list.append([
            vertices_list.index(obj["triangle"][0])+1,
            vertices_list.index(obj["triangle"][1])+1,
            vertices_list.index(obj["triangle"][2])+1
        ])

print(*triangle_list, sep=',\n')

print(len(vertices_list), len(triangle_list))