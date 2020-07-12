import time

start = time.time()
path = r"C:\Users\Hp\Desktop\elewacja.dxf"
import dxfgrabber
import pickle


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
    calc_data = abs(temp_size[0][0] - temp_size[1][0])
    temp_data_size.append(calc_data)
    calc_data = abs(temp_size[0][1] - temp_size[3][1])
    temp_data_size.append(calc_data)
    return temp_data_size


# defines your dxf object
dxf = dxfgrabber.readfile(path)
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

# print(level_temp_data)
# print(elevation_temp_data)
# print()
# print(level_temp_data)
# print(temp_data)
left_border = 3000
right_border = 12000
dict_module_coordinate = {}
list_module_coordinate = []
print(elevation_temp_data)
for entity in dxf.entities:
    if entity.dxftype == "INSERT":
        x_coordinate = int(entity.insert[0])
        y_coordinate = int(entity.insert[1])
        if "BL." in entity.name:
            dict_module_coordinate = {}
            dict_module_coordinate['name'] = entity.name
            dict_module_coordinate['X'] = x_coordinate
            dict_module_coordinate['Y'] = y_coordinate
            dict_module_coordinate['level'] = ''
            dict_module_coordinate['elev'] = ''
            for k_b, v_b in elevation_temp_data.items():
                if dict_module_coordinate['X'] in range(k_b - left_border, k_b + right_border):
                    dict_module_coordinate['elev'] = v_b.replace("{", "").replace("}", "")
                    list_module_coordinate.append(dict_module_coordinate)

# with open('file_data_X_Y.txt','wb') as file_X_Y:
#    file_X_Y.write(pickle.dumps(list_module_coordinate())
# print("ok")

# x_data=open('file_data_X_Y.txt','rb'):
# pickle_X_data=pickle.load(x_data)
# x_data.close()
# print(level_temp_data)
for i in list_module_coordinate:
    Y_temp = int(i['Y'])
    temp_data = []
    temp_data = {abs(k - Y_temp): v for k, v in level_temp_data.items()}
    temp_lambda = lambda temp_data: min(temp_data.items())
    i['level'] = temp_lambda(temp_data)[1].replace("{", "").replace("}", "")

with open('file_data_X_Y.txt', 'w') as file_X_Y:
    file_X_Y.write(str(list_module_coordinate))

module_data = {}
file = open('file_data.txt', 'w')
# you can access info within each block with the following loop:
# this will print a new line of points for each polyline it finds in each block

for blocks in dxf.blocks:
    if "BL." in blocks.name:
        temp_x_y = []
        for elements in blocks:
            if elements.dxftype == "LWPOLYLINE":
                file.write(export_data("LWPOLYLINE", blocks.name, elements.points))
                temp = []
                temp = export_data_X_Y(elements.points)
                if len(temp) == 4:
                    module_data[blocks.name] = module_size(temp)
            if elements.dxftype == "LINE":
                temp_x_y.append(elements.start)
                temp_x_y.append(elements.end)
        if len(temp_x_y) != 0:
            file.write(export_data("LINE", blocks.name, temp_x_y))
file.close()
end = time.time()
print(end - start)
