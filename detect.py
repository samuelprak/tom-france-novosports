import cv2 as cv

ellipse_element = cv.getStructuringElement(cv.MORPH_ELLIPSE, (15, 15))
background_subtractor = cv.createBackgroundSubtractorMOG2()

def remove_background(image):
    mask = background_subtractor.apply(image)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, ellipse_element)
    mask = cv.blur(mask, (5, 5))
    image = cv.bitwise_and(image, image, mask=mask)

    return image

def get_players(image):
    players = []

    image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    only_hats = cv.inRange(image, (0, 115, 200), (180, 255, 255))

    mask = cv.morphologyEx(only_hats, cv.MORPH_OPEN, ellipse_element)
    mask = cv.blur(mask, (10, 10))
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        M = cv.moments(cnt)
        area = M['m00']

        x,y,w,h = cv.boundingRect(cnt)
        ROI = image[y:y+h, x:x+w]
        mean_hue = np.median(ROI[:,:,0])

        x = int(M["m10"] / M["m00"])
        y = int(M["m01"] / M["m00"])

        player = {
            "position": (x, y),
            "area": M['m00']
        }

        if mean_hue in range(150, 160):
            player["color"] = "pink"
        elif mean_hue in range(5, 15):
            player["color"] = "orange"
        elif mean_hue in range(40, 65):
            player["color"] = "green"
        else:
            player["color"] = "error"

        players.append(player)

    return players


def detect_players(image):
    # Remove BG
    image = remove_background(image)

    # Convert to HSV
    image = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    # get players
    players = get_players(image)

    return players
