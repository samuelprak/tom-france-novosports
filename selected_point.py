from distance import find_nearby_point_index
from models.field import Field


class SelectedPoint:
    is_selected = False
    index = None

    def __init__(self, field: Field):
        self.field = field

    def select_nearby_point(self, points, x, y):
        if self.is_selected:
            self.unselect()
            return True

        nearby_field_point_index = find_nearby_point_index(points, (x, y))

        if nearby_field_point_index is not None:
            self.is_selected = True
            self.index = nearby_field_point_index
            return True
        return False

    def on_move(self, point):
        if self.is_selected:
            self.field.set_point_at(self.index, point)

    def on_delete(self):
        if self.is_selected:
            self.field.delete_at(self.index)
            self.unselect()

    def unselect(self):
        self.is_selected = False
        self.index = None
