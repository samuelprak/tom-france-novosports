from distance import transformation_matrix


class Field:
    points = [(722, 268), (1119, 268), (76, 761), (1725, 742)]

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
