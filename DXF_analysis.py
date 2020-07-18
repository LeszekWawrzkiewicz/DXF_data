import time
import math

start = time.time()
path = r"C:\Users\Hp\Desktop\elewacja.dxf"
import dxfgrabber
from operator import itemgetter


def export_data(shape_name, block_name, block_points):
    return f"{block_name}\{shape_name}\{export_data_X_Y(block_points)}\{len(export_data_X_Y(block_points))}\n"


def export_data_X_Y(block_points):
    final_temp_data = []
    temp_data = []
    for q in block_points:
        temp_data = []
        temp_data.append(int(q[0]))
        temp_data.append(int(q[1]))
        internal_temp_data = tuple(temp_data)
        final_temp_data.append(internal_temp_data)
    return final_temp_data


def module_size(temp_size):
    temp_data_size = []
    calc_data = int(abs(temp_size[0][0] - temp_size[2][0]))
    temp_data_size.append(calc_data)
    calc_data = int(abs(temp_size[0][1] - temp_size[2][1]))
    temp_data_size.append(calc_data)
    return temp_data_size


dxf = dxfgrabber.readfile(path)
temp_code_W_H_total = []

file_X_Y = open('file_data_X_Y.txt', 'w')
for blocks in dxf.blocks:
    if blocks.name:
        for elements in blocks:
            temp_code_W_H = {}
            if elements.dxftype == "LWPOLYLINE":
                temp_code_W_H['code'] = blocks.name
                temp_code_W_H['B'] = module_size(elements.points)[0]
                temp_code_W_H['H'] = module_size(elements.points)[1]
                temp_code_W_H_total.append(temp_code_W_H)
                file_X_Y.write(str(temp_code_W_H))
                file_X_Y.write('\n')
file_X_Y.close()
level_temp_data = {}
elevation_temp_data = {}
# print(dxf.entities)
levels_data_base = set()
for entity in dxf.entities:
    if entity.dxftype == "MTEXT":
        if "ELEWACJA" in entity.raw_text:
            elevation_temp_data[int(entity.insert[0])] = entity.raw_text.strip()
        if entity.raw_text[1] == "P":
            level_temp_data[int(entity.insert[1])] = entity.raw_text.replace("{", "").replace("}", "")

left_border = 3000
right_border = 12000
dict_module_coordinate = {}
list_module_coordinate = []
temp_global_list = []
temp_local_list = ()
radius = ''
file_X_Y = open('temp_global_list.txt', 'w')
for entity in dxf.entities:
    if entity.dxftype == "INSERT":
        x_coordinate = int(entity.insert[0])
        y_coordinate = int(entity.insert[1])
        if type(entity.name) is str:
            dict_module_coordinate = {}
            dict_module_coordinate['name'] = entity.name
            # dict_module_coordinate['X'] = x_coordinate
            # dict_module_coordinate['Y'] = y_coordinate
            x = list(filter(lambda W_data: W_data['code'] == entity.name, temp_code_W_H_total))[0][
                'B']  # szerokość modułu
            y = list(filter(lambda W_data: W_data['code'] == entity.name, temp_code_W_H_total))[0][
                'H']  # wysokość modułu
            # dict_module_coordinate['X_R'] = x + x_coordinate
            temp_local_list = (entity.name, x_coordinate)
            # temp_global_list.append(dict_module_coordinate)
            radius = math.sqrt((x / 2) ** 2 + (y / 2) ** 2)

            # temp_global_list.append(dict_module_coordinate)
            file_X_Y.write(str(temp_local_list))
            dict_module_coordinate['C_X'] = int(
                x_coordinate + x / 2)  # C_X-wyznaczenie środka współrzędnej środka ramki na współrzędnej X
            dict_module_coordinate['C_Y'] = int(
                y_coordinate + y / 2)  # C_Y-wyznaczenie środka współrzędnej środka ramki na współrzędnej Y
            dict_module_coordinate['radius'] = int(radius)
            dict_module_coordinate['N'] = 0  # N-neighbour
            temp_global_list.append(dict_module_coordinate)
            temp_local_list = ()

file_X_Y.close()

sorted_list = sorted(temp_global_list, key=itemgetter("C_X", "C_Y"))
file_X_Y = open('temp_global_list_total.txt', 'w')
for i in sorted_list:
    file_X_Y.write(f"{str(i)}\n")
    # print(i)
file_X_Y.close()

temp_id = 1
mirror_sorted_list = sorted_list
sorted_list[0]['N'] = temp_id
for key, frame in enumerate(sorted_list):

    for temp_key, temp_frame in enumerate(mirror_sorted_list):
        if temp_key != key and frame['N'] != temp_frame['N']:
            distance_X = temp_frame['C_X'] - frame['C_X']
            distance_Y = temp_frame['C_Y'] - frame['C_Y']
            distance_r = temp_frame['radius'] + frame['radius']
            if distance_r >= distance_Y:
                frame['N'] = temp_id
                temp_frame['N'] = frame['N']
                print(frame)
            break

# for i in sorted_list:
#    print(i)

end = time.time()
print(end - start)
