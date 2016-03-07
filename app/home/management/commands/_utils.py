from math import factorial


def combinations_nb(n, r):
    return int(factorial(n) / (factorial(n - r) * factorial(r)))


# Returns a box containing the room polygon and reorganises rectangle coordinates
def boundary_box(coords):
    # initializes box with initial point : box[minX, minY, maxX, maxY]
    bbox = [coords[0], coords[1], coords[0], coords[1]]

    # Skips initial point and searches for greater or smaller values
    for i in range(2, len(coords)):
        val = coords[i]

        if i % 2 == 0:  # X value
            bbox[0] = (val if val < bbox[0] else bbox[0])  # found a new X min
            bbox[2] = (val if val > bbox[2] else bbox[2])  # found a new X max
        else:  # Y value
            bbox[1] = (val if val < bbox[1] else bbox[1])  # found a new Y min
            bbox[3] = (val if val > bbox[3] else bbox[3])  # found a new X max

    return bbox
