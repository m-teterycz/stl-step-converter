import struct
from array import array
import os

def stl_type(data):
    if 'vertex' in data:
        return 'ascii'
    return 'binary'

def read_data(path):
    if determine_filetype(path) == "A":
        return format_data_ascii(path)
    else:
        return format_data_binary(path)

def determine_filetype(path):
    with open(path, "rb") as f:
        data = f.read()
        file_size = os.path.getsize(path)
        triangle_count = int.from_bytes(data[80:84], 'little')

        if 84 + triangle_count * 50 != file_size:
            return "A"
        return "B"


def format_data_ascii(path):
    formatted_data = array("f")
    with open(path, 'r') as f:
        for line in f:
            try:
                if 'vertex' == line.strip()[0:6].lower(): # the strip and parsing are used to make sure the name doesnt have vertex in it.
                    line = line.strip().split()
                    vertices = line[1:]
                    formatted_data.extend((float(vertices[0]), float(vertices[1]), float(vertices[2])))
            except:
                raise Exception("Couldn't read the ASCII Stl")
    return formatted_data
    
def format_data_binary(path):
    with open(path, 'rb') as f:
        data = f.read()
        triangle_count = int.from_bytes(data[80:84], 'little')

        formatted_data = array("f")

        if triangle_count != (len(data) - 84) // 50:
            raise Exception("Invalid Stl Size")
        
        for i in range(triangle_count):
            triangle_offset = 50 * i
            
            for j in range(3):
                vertex_offset = 12 * j
                x, y, z = struct.unpack("<fff", (data[84 + 12 + triangle_offset + vertex_offset : 84 + 24 + triangle_offset + vertex_offset]))
                formatted_data.extend((x,y,z))

        return formatted_data
    

def coords_check(coords):
    if len(coords) != 3:
        return False
    
    for coord in coords:
        try:
            float(coord)
        except:
            return False
    return True