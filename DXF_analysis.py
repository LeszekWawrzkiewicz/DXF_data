import time
import math
import sqlite3 as lite

class connection_insert_frame_X_elevation(dict):
    def __init__(self):
        self = dict()

    def add(self, key, value):
        self[key] = value


start = time.time()
path = r"C:\Users\Hp\Desktop\elewacja.dxf"
import dxfgrabber
from operator import itemgetter


def module_size(temp_size):
    '''calculation the sizes of the frame when the frame has the insert point
    in bottom left corner, the main frame must be created by POLYLINE'''
    temp_data_size = []
    calc_data = int(abs(temp_size[0][0] - temp_size[2][0]))
    temp_data_size.append(calc_data)
    calc_data = int(abs(temp_size[0][1] - temp_size[2][1]))
    temp_data_size.append(calc_data)
    return temp_data_size


dxf = dxfgrabber.readfile(path)
temp_code_W_H_total = []

file_X_Y = open('file_data_X_Y.txt', 'w')
'''calculation the main size (width x height; WxH) of the frame'''
for blocks in dxf.blocks:
    if blocks.name:
        for elements in blocks:
            temp_code_W_H = {}
            if elements.dxftype == "LWPOLYLINE":
                temp_code_W_H['code'] = blocks.name
                temp_code_W_H['W'] = module_size(elements.points)[0]
                temp_code_W_H['H'] = module_size(elements.points)[1]
                temp_code_W_H_total.append(temp_code_W_H)
                file_X_Y.write(str(temp_code_W_H))
                file_X_Y.write('\n')
file_X_Y.close()
level_temp_data = {}  # dict of location the "level" text
main_elevation_temp_data = []  # dict of location the "elevation" text
list_module_coordinate = []
''' searching location the text referred to the levels and the elevation, '''
for entity in dxf.entities:
    if entity.dxftype == "MTEXT":
        if "ELEWACJA" in entity.raw_text:
            elevation_temp_data = {}
            elevation_temp_data['X'] = int(entity.insert[0])
            elevation_temp_data['elev'] = entity.raw_text
            main_elevation_temp_data.append(elevation_temp_data)
        if entity.raw_text[1] == "P":
            level_temp_data[int(entity.insert[1])] = entity.raw_text.replace("{", "").replace("}", "")
# print(str(main_elevation_temp_data))
temp_global_list = []
temp_local_list = ()
radius = ''
# file_X_Y = open('temp_global_list.txt', 'w')

'''calculation the location of the middle point of the frames by analysisi insert point of them,
preparing the temporary data about the "radius", the radius is a half of hypotenuse the frame'''

for entity in dxf.entities:
    if entity.dxftype == "INSERT":
        x_coordinate = int(entity.insert[0])
        y_coordinate = int(entity.insert[1])
        if type(entity.name) is str:
            dict_module_coordinate = {}
            dict_module_coordinate['name'] = entity.name
            W_frame = list(filter(lambda W_data: W_data['code'] == entity.name, temp_code_W_H_total))[0][
                'W']  # szerokość modułu
            H_frame = list(filter(lambda H_data: H_data['code'] == entity.name, temp_code_W_H_total))[0][
                'H']  # wysokość modułu
            temp_local_list = (entity.name, x_coordinate)
            radius = math.sqrt((W_frame) ** 2 + (H_frame) ** 2)/2
            # file_X_Y.write(str(temp_local_list))
            dict_module_coordinate['C_X'] = int(
                x_coordinate + W_frame / 2)  # C_X-calculation the middle point in horizontal direction - X-direction
            dict_module_coordinate['C_Y'] = int(
                y_coordinate + H_frame / 2)  # C_Y-calculation the middle point in vertical direction - Y-direction
            dict_module_coordinate['radius'] = int(radius)
            dict_module_coordinate['X1'] = dict_module_coordinate['C_X']-int(radius)
            dict_module_coordinate['X2'] = dict_module_coordinate['C_X']+int(radius)
            dict_module_coordinate['Y1'] = dict_module_coordinate['C_Y']-int(radius)
            dict_module_coordinate['Y2'] = dict_module_coordinate['C_Y']+int(radius)

            dict_module_coordinate['elev'] = ''
            dict_module_coordinate['level'] = ''
            temp_global_list.append(dict_module_coordinate)
            temp_local_list = ()

# file_X_Y.close()

sorted_list = sorted(temp_global_list, key=itemgetter("C_X", "C_Y"))
file_X_Y = open('temp_global_list_total.txt', 'w')
for i in sorted_list:
    file_X_Y.write(f"{str(i)}\n")
    print(i)
file_X_Y.close()

line_list_X = []
'''get the unique value of insert point to X-direction'''
for i in sorted_list:
    line_list_X.append(i['C_X'])
'''sorted list of the unique value of insert X-point on horizontal axis'''
sorted_line_list_X = sorted(set(line_list_X))
'''merging unique insert X-point and the radius'''
total_line_list_X_R = []
'''find the "radius" value for the X-unique value'''
for i in sorted_line_list_X:
    line_list_X_R = {}
    line_list_X_R['X'] = i
    response = next((sub for sub in sorted_list if sub['C_X'] == i), None)
    line_list_X_R['R'] = response['radius']
    total_line_list_X_R.append(line_list_X_R)
counter = 1
'''create dict with data of location the elevation' text'''
X_elev_dict_obj = connection_insert_frame_X_elevation()
'''find the borders between the elevations'''
previous_X = total_line_list_X_R[0]['X']
previous_R = total_line_list_X_R[0]['R']
X_elev_dict_obj.add(previous_X, counter)
for i in total_line_list_X_R[1:]:
    current_X = i['X']
    current_R = i['R']
    temp_connection_insert_frame_X_elevation = {}
    if current_X - previous_X < current_R / 2 + previous_R / 2:
        X_elev_dict_obj.add(current_X, counter)
        previous_X = i['X']
        previous_R = i['R']
    else:
        counter += 1
        previous_X = i['X']
        previous_R = i['R']
        X_elev_dict_obj.add(previous_X, counter)

frame_elevation_level = []
'''sorting location of the "elevation" text'''
sorted_main_elevation_temp_data = sorted(main_elevation_temp_data, key=itemgetter("X"), reverse=False)
'''create a list of data: frame, elevation, level'''
for i in temp_global_list:
    temp_frame_elevation_level = []
    i['elev'] = X_elev_dict_obj[i['C_X']]
    Y_temp = int(i['C_Y'])
    temp_data = []
    temp_data = {abs(k - Y_temp): v for k, v in level_temp_data.items()}
    temp_lambda = lambda temp_data: min(temp_data.items())
    i['level'] = temp_lambda(temp_data)[1].replace("{", "").replace("}", "")
    temp_frame_elevation_level.append(i['name'])
    temp_frame_elevation_level.append(sorted_main_elevation_temp_data[i['elev'] - 1]['elev'].replace("{", "").replace("}", ""))
    temp_frame_elevation_level.append(i['level'])
    frame_elevation_level.append(temp_frame_elevation_level)

    con = lite.connect('test.db')

with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS frame_elevation_level")
    cur.execute("CREATE TABLE frame_elevation_level(name TXT, elev TEXT, level TXT)")
    cur.executemany("INSERT INTO frame_elevation_level VALUES(?, ?, ?)", frame_elevation_level)
with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM frame_elevation_level")
    rows = cur.fetchall()
#    for row in rows:
 #       print(row)

end = time.time()
print(end - start)
