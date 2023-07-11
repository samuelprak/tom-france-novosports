from distance import transformation_matrix


class Field:
    points = [(645, 135), (1174, 132), (185, 613), (1442, 604)]

    def __init__(self, app):
        self.app = app

    def is_defined(self):
        return len(self.points) == 4

    def append(self, point):
        if self.is_defined():
            return

        self.points.append(point)

    def clear(self):
        self.points.clear()

    def set_point_at(self, index, point):
        self.points[index] = point

    def get(self):
        return self.points

    def delete_at(self, index):
        self.points.pop(index)
