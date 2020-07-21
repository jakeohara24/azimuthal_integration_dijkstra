import sys
import numpy as np
import fabio
import networkx as nx
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
import math
import pprint

#file = 'd25_CeO2-00000.tif'
#img = fabio.open(file).data


#Creates random numpy array for testing
test_array = np.random.rand(10,10)

def big_function(image):
    #Make your own bool array, which will correspond to the bools in the intensity array
    bool_array = np.broadcast_to(False, image.shape)


    #This will take each pixel coordinate, as a key, and match its corresponding intensity to a value in a dictionary
    height_img = image.shape[0]
    width_img = image.shape[1]


    height_bool = bool_array.shape[0]
    width_bool = bool_array.shape[1]

    total_coordinates_list = []
    intensities_list = []
    #Two dictionaries, one with intensities, one with booleans
    both_dict = {}
    ###Figure out how to make all false firts, thenmove to this part
    
    def get_image_edges(image):
        height, width = image.shape
        edge_pixels = []
        edge_pixels.extend([(0, y) for y in range(height)])
        edge_pixels.extend([(x, height_img) for x in range(width)])
        edge_pixels.extend([(width_img, y) for y in range(height)])
        edge_pixels.extend([(x, 0) for x in range(width)])
        #print("These are the edges of your image", edge_pixels)
        return edge_pixels

    #Coordinates for intensities
    for y in range(height_img) and range (height_bool):
        for x in range(width_img) and range(width_bool):
            pixel = image.data[x,y]
            bool_val = bool_array[x,y]
            both_dict.update({(x,y): [bool_val, pixel]})

    #print(list(both_dict.items())[1])

    values_list = []
    values_coordinates = []

    def find_start_values(x, y):
        starting_bool_and_intensity = both_dict[(x, y)]
        values_list.append(starting_bool_and_intensity)
        #starting_point = both_dict.keys((x, y))
        values_coordinates.append((x, y))

        #was getting stuck on flipping the bool value: fixed with smaller_list[0] = not smaller_list[0]
        #for smaller_list in values_list:
        #    smaller_list[0] = True

        #print(values_list)


    def getadjacent_pixels(x, y):
        good_list = []
        a_p = (x-1, y), (x, y-1), (x+1, y), (x, y+1), (x-1, y-1), (x+1, y+1), (x-1, y+1), (x+1, y-1)
        
        for px, py in a_p:
            if 0 <= px < width_img:
                if 0 <= py < height_img:
                    good_list.append((px, py))
                       
        return good_list
    
    shortest_path_point_dictionaries = {}
    for edge_starting_point in get_image_edges(image):
        #Creates dictionaries to store list of least 
        shortest_path_point_dictionaries.update({edge_starting_point: []})
    

    pixels_to_visit = [(np.ceil(height_img/2), np.ceil(width_img/2))]
    
    every_single_pixel_dictionary = {}
    for y in range(height_img) and range (height_bool):
        for x in range(width_img) and range(width_bool):
            every_single_pixel_dictionary.update({(x, y): [math.inf, []]})
    
    center_pixel = (np.ceil(height_img/2), np.ceil(width_img/2))
    every_single_pixel_dictionary[center_pixel] = [both_dict[center_pixel][1], [center_pixel]]
    
    while len(pixels_to_visit) > 0:
        pixel_xy = pixels_to_visit.pop()
        both_dict[pixel_xy][0] = True
        path_intensity, path = every_single_pixel_dictionary[pixel_xy]
        #print("path:", path, pixel_xy)
        #print("path intensity", path_intensity)
        
        #print("this pixel", pixel[0], pixel[1])
        
        #This line is producing the None
        #print(find_start_values(pixel_xy[0], pixel_xy[1]))
        
        #Thing in curly braces is interprated as the varriable
        #print(f"pixel = {pixel}")
        adjacents = getadjacent_pixels(pixel_xy[0], pixel_xy[1])
        #print(f"adjacents = {adjacents}")
        
        for adjacent_pixel in adjacents:
            pixel_value = both_dict[adjacent_pixel]
            if pixel_value[0] == False:
                pixels_to_visit.append(adjacent_pixel)
            intensity_sum = path_intensity + both_dict[adjacent_pixel][1]
        
            if intensity_sum < every_single_pixel_dictionary[adjacent_pixel][0]:
                worst_path = every_single_pixel_dictionary[adjacent_pixel][1]
                best_path = path + [adjacent_pixel]
                every_single_pixel_dictionary[adjacent_pixel][1] = best_path
                every_single_pixel_dictionary[adjacent_pixel][0] = intensity_sum
                #print("best path", best_path)
                #print("intensity for that path:", intensity_sum)
            #else:
                #print("found a worse path for", adjacent_pixel)
                

    adjacent_pixel_coordinates = getadjacent_pixels(np.ceil(height_img/2), np.ceil(width_img/2))
    values_coordinates.extend(adjacent_pixel_coordinates)
    
    #as we go along, math.inf will be replaced by the the sum of the intensities of every pixel in the list
    #and the list will be the list will contain the pixel coordinates
    
    
    path_list = []

    
    #was getting stuck on flipping the bool value: fixed with value[0] = not value[0]
    for key, value in both_dict.items():
        if key in values_coordinates and value[0] == False:
            value[0] = not value[0]

    #Some of these repeat at overlapping points
    #pprint.pprint(every_single_pixel_dictionary)
    #print(every_single_pixel_dictionary.keys())
    final_paths_list = []
    for q in get_image_edges(image):
        if q in every_single_pixel_dictionary.keys():
            #print("Here are the matching points:", q)
            edge_from_center = every_single_pixel_dictionary[q]
            final_paths_list.append(edge_from_center)
            #edge_from_center_array = np.array(edge_from_center)
            #print(edge_from_center)
            
            #This can help keep you organized
            #print("The lowest intensity path to get from center to the edge", q, "is", every_single_pixel_dictionary[q])
            
    #This list contains the final paths
    print(final_paths_list)
    
            #print("The lowest intensity path to get from center to the edge", q, "is", every_single_pixel_dictionary[q])
    return final_paths_list
