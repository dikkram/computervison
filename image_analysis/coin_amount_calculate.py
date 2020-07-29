"""
Coin recognition, real life application
task: calculate the value of coins on picture
"""

import cv2
import numpy as np

def detect_coins():
    coins = cv2.imread('../input_image/koruny.jpg', 1)
    width, height, channel = coins.shape

    if width < height:
        short = width
    else:
        short = height

    gray = cv2.cvtColor(coins, cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(gray, 9)
    circles = cv2.HoughCircles(
        img,  # source image
        cv2.HOUGH_GRADIENT,  # type of detection
        1,
        40,
        param1=70,
        param2=50,
        minRadius=30,  # minimal distance between two centers
        maxRadius=short,  # max distance between two centers
    )

    coins_copy = coins.copy()
    radius = []

    for detected_circle in circles[0]:
        x_coor, y_coor, detected_radius = detected_circle
        coins_detected = cv2.circle(
            coins_copy,
            (int(x_coor), int(y_coor)),
            int(detected_radius),
            (0, 0, 255),
            2,
        )

    cv2.imwrite("../output_image/coin_detection/koruny_test_Hough.jpg", coins_detected)

    return circles

def calculate_amount():
    koruny = {
        "jednokorun": {
            "value": 1,
            "radius": 20,
            "ratio": 1,
            "count": 0,
        },
        "dvoukorun": {
            "value": 2,
            "radius": 21.5,
            "ratio": 1.075,
            "count": 0,
        },
        "pětikorun": {
            "value": 5,
            "radius": 23,
            "ratio": 1.15,
            "count": 0,
        },
        "desetikorun": {
            "value": 10,
            "radius": 24.5,
            "ratio": 1.225,
            "count": 0,
        },
        "dvacetikorun": {
            "value": 20,
            "radius": 26,
            "ratio": 1.3,
            "count": 0,
        },
        "padesátikorun": {
            "value": 50,
            "radius": 27.5,
            "ratio": 1.375,
            "count": 0,
        },
    }

    circles = detect_coins()
    radius = []
    coordinates = []

    for detected_circle in circles[0]:
        x_coor, y_coor, detected_radius = detected_circle
        radius.append(detected_radius)
        coordinates.append([x_coor, y_coor])

    smallest = min(radius)
    tolerance = 0.03
    total_amount = 0

    coins_circled = cv2.imread('../output_image/coin_detection/koruny_test_Hough.jpg', 1)
    font = cv2.FONT_HERSHEY_SIMPLEX

    for coin in circles[0]:
        ratio_to_check = coin[2] / smallest
        coor_x = coin[0]
        coor_y = coin[1]
        for koruna in koruny:
            value = koruny[koruna]['value']
            if abs(ratio_to_check - koruny[koruna]['ratio']) <= tolerance:
                koruny[koruna]['count'] += 1
                total_amount += koruny[koruna]['value']
                cv2.putText(coins_circled, str(value), (int(coor_x), int(coor_y)), font, 1,
                            (255, 255, 255), 2)

    print(total_amount)
    print(koruny)


    cv2.imwrite("../output_image/coin_detection/koruny_hodnota.jpg", coins_circled)


calculate_amount()