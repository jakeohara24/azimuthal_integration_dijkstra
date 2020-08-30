import sys
import numpy as np
import fabio
import networkx as nx
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
import math
import pprint

#Use fabio to open tif files, then pass them to the function:  
#open tif files with fabio.open('file_name').data
def dijkstra_paths(image):
    #Makes a bool array, with same dimensions as input image
    bool_array = np.broadcast_to(False, image.shape)


    #Dimensions of image
    height_img = image.shape[0]
    width_img = image.shape[1]

    #Dimensions of bool array
    height_bool = bool_array.shape[0]
    width_bool = bool_array.shape[1]

    total_coordinates_list = []
    intensities_list = []

    both_dict = {}

    #Finds the edge coordinates for the input image
    def get_image_edges(image):
        height, width = image.shape
        edge_pixels = []
        edge_pixels.extend([(0, y) for y in range(height)])
        edge_pixels.extend([(x, (height_img-1)) for x in range(width)])
        edge_pixels.extend([((width_img-1), y) for y in range(height)])
        edge_pixels.extend([(x, 0) for x in range(width)])

        return edge_pixels
    
    values_list = []
    values_coordinates = []
    
    #Finds the center pixel; in Dijkstra's algorithm, this is considered to be the starting point
    def find_start_values(x, y):
        starting_bool_and_intensity = both_dict[(x, y)]
        values_list.append(starting_bool_and_intensity)
        #starting_point = both_dict.keys((x, y))
        values_coordinates.append((x, y))

    #Finds the pixels which lie adjacent to the currently visited pixel; up, down, left, right
    def getadjacent_pixels(pixel):
        x = pixel[0]
        y = pixel[1]
        good_list = []
        a_p = (x-1, y), (x, y-1), (x+1, y), (x, y+1)
        
        for px, py in a_p:
            if 0 <= px < width_img:
                if 0 <= py < height_img:
                    good_list.append((px, py))
                       
        return good_list
    

    #Adds the center, starting pixel to this list of pixels to visit
    pixels_to_visit = [(np.floor(height_img/2), np.floor(width_img/2))]
    
    #Create dictionary for all the paths
    total_paths_dict = {}
    
    #Create a set for the unvisited pixels
    unvisited_set = set()
    
    #Designate the center
    center_pixel = (int(np.floor(height_img/2)), int(np.floor(width_img/2)))
    
    #The total_paths_dictionary will contain the coordinate on the image, the sum of the intensities, and a list of pixels which compose that path
    for y in range(height_img):
        for x in range(width_img):
            unvisited_set.add((int(x), int(y)))
            #All unvisited pixels have a cost of infinity
            total_paths_dict.update({(x, y): {'path intensity': math.inf, 'path': [center_pixel]}})
    
    #However the starting pixel has cost of 0, as per Dijkstra's algorithm
    total_paths_dict[center_pixel]['path intensity'] = 0
    
    pixels_to_visit = [center_pixel]
    #while loop begins: while there are items in the pixels to visit list...
    while len(pixels_to_visit) > 0:
        #Removes current node from the unvisited set
        #Takes the first thing off the list. Note: in previous version, it took the last thing from the list
        current_pixel = pixels_to_visit.pop(0)
        
        if current_pixel in unvisited_set:
            path_intensity = total_paths_dict[current_pixel]['path intensity']
            path = total_paths_dict[current_pixel]['path']
    
            adjacents = getadjacent_pixels(current_pixel)
        
            for adjacent_pixel in adjacents:
                #Checks if the destination has been visited. If not, add it to the list of pixels to visit
                if adjacent_pixel in unvisited_set:
                    pixels_to_visit.append(adjacent_pixel)
                    tentative_intensity_sum = total_paths_dict[current_pixel]['path intensity'] + image[adjacent_pixel]
                    #print(total_paths_dict[adjacent_pixel]['path'])
                    #print(total_paths_dict[adjacent_pixel]['path intensity'])
            
                    if tentative_intensity_sum < total_paths_dict[adjacent_pixel]['path intensity']:
                        best_path = path + [adjacent_pixel]
                        #print('best path', best_path)
                        total_paths_dict[adjacent_pixel]['path intensity'] = tentative_intensity_sum
                        total_paths_dict[adjacent_pixel]['path'] = best_path

                        #print('intensity sum', tentative_intensity_sum)
                    
            unvisited_set.remove(current_pixel)
            
    adjacent_pixel_coordinates = getadjacent_pixels(center_pixel)
    values_coordinates.extend(adjacent_pixel_coordinates) 
    
    path_list = []

    
    final_paths_list = []
    just_the_paths_list = []
    for q in get_image_edges(image):
        if q in total_paths_dict.keys():
            #print("Here are the matching points:", q)
            edge_from_center = total_paths_dict[q]
            final_paths_list.append(edge_from_center)
    
    for g in final_paths_list:
        just_the_paths_list.append(g['path'])
    #print(just_the_paths_list)
    
    point_set = {item for path in just_the_paths_list for item in path}
    
    
    bools = [[not (i, j) in point_set for i in range(height_img)] for j in range(width_img)]

    masked = [[1*bools[y][x] for x, pixel in enumerate(image_row)] for y, image_row in enumerate(image)]
      
    return masked
    

