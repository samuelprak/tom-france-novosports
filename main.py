import threading

import cv2 as cv
import numpy as np

from constants import (
    COLORS,
    ENABLE_WEB,
    ORANGE_COLOR,
    PLAYER_DETECTION_SCALE,
    RED_COLOR,
    VIDEO_CAPTURE_SOURCE,
    WHITE_COLOR,
)
from detect import detect_players
from display import (
    display_current_timestamp,
    display_point,
    display_points,
    display_zone,
)
from distance import destination_point, points_too_close, transformation_matrix
from models.field import Field
from selected_point import SelectedPoint
from web import app, queue

cap = cv.VideoCapture(VIDEO_CAPTURE_SOURCE)


class FieldDetector:
    def __init__(self):
        self.field = Field(self)
        self.move_point = SelectedPoint(self.field)
        self.frame = None

    def transform_frame(self, frame, M):
        height, width = frame.shape[:2]
        return cv.warpPerspective(frame, M, (width, height))

    # INTERFACE

    def click_event(self, event, x, y, flags, params):
        if event == cv.EVENT_LBUTTONDOWN:
            if self.move_point.select_nearby_point(self.field.points, x, y):
                return
            self.field.append((x, y))
        if event == cv.EVENT_MOUSEMOVE:
            self.move_point.on_move((x, y))

    # LOOP FUNCTIONS

    def handle_key(self, key):
        if key == ord("q"):
            exit()
        elif key == ord("r"):
            self.field.clear()
        elif key == 32:
            while True:
                key = cv.waitKey(10)
                if key == 32:
                    break
        elif key == 2:
            cap.set(
                cv.CAP_PROP_POS_FRAMES,
                cap.get(cv.CAP_PROP_POS_FRAMES) - cap.get(cv.CAP_PROP_FPS),
            )
        elif key == 3:
            cap.set(
                cv.CAP_PROP_POS_FRAMES,
                cap.get(cv.CAP_PROP_POS_FRAMES) + cap.get(cv.CAP_PROP_FPS),
            )
        elif key == 127:
            self.move_point.on_delete()

    def display_player_points(self, frame, players, player_indexes_too_close):
        for i, (color, point) in enumerate(players):
            color = RED_COLOR if i in player_indexes_too_close else COLORS[color]

            display_point(frame, point, color=color, text=str(i))

    def display_field_points(self, frame, field_points):
        height, width = frame.shape[:2]

        M = transformation_matrix(width, height, field_points)
        M_inv = np.linalg.inv(M)

        field_frame = self.transform_frame(frame, M)
        field_frame = cv.resize(
            field_frame,
            (np.array([width, height]) * PLAYER_DETECTION_SCALE).astype(int),
        )

        detected_players = detect_players(field_frame)
        players = detected_players.items()
        player_field_points = detected_players.values()

        player_indexes_too_close = points_too_close(frame, player_field_points)

        self.display_player_points(field_frame, players, player_indexes_too_close)
        self.display_player_points(
            frame,
            [
                (
                    type,
                    destination_point(
                        np.array(p) * (1 / PLAYER_DETECTION_SCALE), M_inv
                    ),
                )
                for type, p in players
            ],
            player_indexes_too_close,
        )
        if not ENABLE_WEB:
            cv.imshow("Field", field_frame)

        display_zone(frame, field_points)

    def get_field_point_color(self, field_point_index):
        if self.move_point.index == field_point_index:
            return ORANGE_COLOR
        return WHITE_COLOR

    def main(self):
        while cap.isOpened():
            ret, frame = cap.read()
            self.frame = frame

            if not ret:
                cap.set(cv.CAP_PROP_POS_FRAMES, 0)
                continue

            if self.field.is_defined():
                self.display_field_points(frame, self.field.points)

            display_points(
                frame,
                self.field.points,
                color_per_point=[
                    self.get_field_point_color(i)
                    for i, _ in enumerate(self.field.points)
                ],
            )
            display_current_timestamp(cap, frame)

            queue.put(frame.copy())

            cv.setMouseCallback("Image", self.click_event)  # type: ignore
            if not ENABLE_WEB:
                cv.imshow("Image", frame)
            self.handle_key(cv.waitKey(10))


def start_field_detector():
    field_detector = FieldDetector()
    field_detector.main()


def main():
    if ENABLE_WEB:
        t = threading.Thread(target=start_field_detector)
        t.daemon = True
        t.start()

        app.run(debug=True)
    else:
        start_field_detector()


main()
