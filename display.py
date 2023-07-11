import cv2 as cv
from constants import BLACK_COLOR


def display_zone(frame, points):
    lines = [(0, 1), (1, 3), (3, 2), (2, 0)]
    for i in range(4):
        cv.line(frame, points[lines[i][0]], points[lines[i][1]], (0, 0, 255), 2)


def display_point(frame, point, color, text=""):
    cv.circle(frame, (point[0] + 2, point[1] + 2), 10, (0, 0, 0), -1)
    cv.circle(frame, point, 10, color, -1)
    cv.putText(
        frame,
        text,
        (point[0] + 12, point[1] + 12),
        cv.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 0),
        2,
        cv.LINE_AA,
    )
    cv.putText(
        frame,
        text,
        (point[0] + 10, point[1] + 10),
        cv.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        2,
        cv.LINE_AA,
    )


def display_points(frame, points, color_per_point: list):
    for i, point in enumerate(points):
        color = color_per_point[i]
        display_point(frame, point, color, str(i))


def display_current_timestamp(cap, frame):
    cv.putText(
        frame,
        str(round(cap.get(cv.CAP_PROP_POS_FRAMES) / cap.get(cv.CAP_PROP_FPS), 2)),
        (10, 50),
        cv.FONT_HERSHEY_SIMPLEX,
        1,
        BLACK_COLOR,
        2,
        cv.LINE_AA,
    )
