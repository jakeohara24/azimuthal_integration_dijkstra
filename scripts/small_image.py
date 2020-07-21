import time

import numpy as np

from azimuthal_integration_dijkstra import Dijkstra


def main():

    small_image = np.random.rand(500, 500)
    t0 = time.time()
    path_list = Dijkstra.big_function(small_image)
    t1 = time.time()
    print(f"time spent: {t1-t0:.3f}s")


if __name__ == "__main__":
    main()
