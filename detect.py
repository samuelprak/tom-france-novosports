import cv2 as cv

ellipse_element = cv.getStructuringElement(cv.MORPH_ELLIPSE, (15, 15))
background_subtractor = cv.createBackgroundSubtractorMOG2()

colors = [
    {
        "name": "green",
        "low_range": (33, 128, 0),
        "high_range": (55, 255, 255),
        "debug_color": (0, 255, 0),
    },
    {
        "name": "pink",
        "low_range": (145, 75, 20),
        "high_range": (175, 255, 255),
        "debug_color": (0, 0, 255),
    },
]


def remove_background(image):
    mask = background_subtractor.apply(image)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, ellipse_element)
    mask = cv.blur(mask, (5, 5))
    image = cv.bitwise_and(image, image, mask=mask)

    return image


def get_center_from_range(image, low_range, high_range):
    mask = cv.inRange(image, low_range, high_range)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, ellipse_element)
    mask = cv.dilate(mask, ellipse_element, iterations=2)
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # TODO: Keep only biggest contour (instead of the first one)
    if not contours:
        return (-1, -1)

    M = cv.moments(contours[0])
    x = int(M["m10"] / M["m00"])
    y = int(M["m01"] / M["m00"])
    return x, y


def get_players(image):
    players = {}

    for color in colors:
        x, y = get_center_from_range(image, color["low_range"], color["high_range"])
        if x != -1 and y != -1:
            # cv.circle(raw, (x, y), 20, color["debug_color"], 2)
            name = color["name"]
            players[name] = (x, y)

    return players


def detect_players(image):
    # Remove BG
    image = remove_background(image)

    # Convert to HSV
    image = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    # get players
    players = get_players(image)

    return players
