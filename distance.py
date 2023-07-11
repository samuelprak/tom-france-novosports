import numpy as np
import cv2 as cv
from constants import WARNING_DISTANCE, FIELD_HEIGHT, FIELD_WIDTH


def find_nearby_point_index(points: list, point):
    for i, p in enumerate(points):
        if np.linalg.norm(np.array(p) - np.array(point)) < 40:
            return i
    return None


def destination_point(p, M):
    px = (M[0][0] * p[0] + M[0][1] * p[1] + M[0][2]) / (
        (M[2][0] * p[0] + M[2][1] * p[1] + M[2][2])
    )
    py = (M[1][0] * p[0] + M[1][1] * p[1] + M[1][2]) / (
        (M[2][0] * p[0] + M[2][1] * p[1] + M[2][2])
    )
    return (int(px), int(py))


def transformation_matrix(width, height, points):
    src = np.float32(points)
    dst = np.float32(
        [(0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1)]  # type: ignore
    )
    return cv.getPerspectiveTransform(src, dst)


def frame_to_field_plan(frame, frame_point):
    x, y = frame_point
    frame_height, frame_width = frame.shape[:2]
    return ((x * FIELD_WIDTH) / frame_width, (y * FIELD_HEIGHT) / frame_height)


def field_distance_between_all_frame_points(frame, points: list):
    distance_matrix = [[0 for _ in range(len(points))] for _ in range(len(points))]
    for i, point1 in enumerate(points):
        for j, point2 in enumerate(points):
            if i != j:
                field_point1 = frame_to_field_plan(frame, point1)
                field_point2 = frame_to_field_plan(frame, point2)
                distance_matrix[i][j] = np.linalg.norm(  # type: ignore
                    np.array(field_point1) - np.array(field_point2)
                )
    return distance_matrix


def add_players_too_close(frame, players):
    points = [p["position"] for p in players]

    distance_matrix = field_distance_between_all_frame_points(frame, points)
    points_too_close = set()
    for i, row in enumerate(distance_matrix):
        for j, distance in enumerate(row):
            if i != j and distance < WARNING_DISTANCE:
                points_too_close.add(tuple(sorted([i, j])))

    # return [{**p, "too_close": } for p in players]
