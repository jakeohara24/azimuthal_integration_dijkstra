import numpy as np
import pprint

import azimuthal_integration_dijkstra.Dijkstra as dijkstra


def test_10x10_random_image():
    test_array = np.random.rand(10, 10)

    path_list = dijkstra.big_function(image=test_array)
    pprint.pprint(path_list)
    assert len(path_list) == 42


def test_known_image():
    test_array = np.array([
        [1.0, 1.0, 1.0],
        [1.0, 1.0, 1.0],
        [1.0, 1.0, 1.0]
    ])

    path_list = dijkstra.big_function(image=test_array)
    first_path = path_list[0]
    first_path_starting_point = first_path[1][0]
    assert first_path_starting_point == (1.0, 1.0)
    pprint.pprint(path_list)
    assert len(path_list) == 12
