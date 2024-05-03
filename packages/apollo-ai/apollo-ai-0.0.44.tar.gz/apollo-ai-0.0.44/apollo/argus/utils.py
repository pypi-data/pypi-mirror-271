import cv2
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
from math import cos, sin
import numpy as np
import os


def filter_video_data(distances_data: list[list[float]], normalize: bool) -> pd.DataFrame:  # Name's not accurate
    """
    Not really sure yet what it does

    :param distances_data:
    :param normalize:
    :return:
    """
    try:
        df = pd.DataFrame(distances_data, columns=["Distance", "Timestamp"])
        df = df.sort_values(by=["Timestamp"])

        # Calculate the normalization based on min and max values
        if normalize:
            max_value = df['Distance'].max()
            min_value = df['Distance'].min()
            df['Distance'] = (df['Distance'] - min_value) / (max_value - min_value)

        # Smooth the data using scipy and Savitzky-Golay Filter
        df['Distance'] = signal.savgol_filter(df["Distance"], 260, 3)

        return df
    except Exception as e:
        raise Exception("Error normalizing the data: {0}".format(e))


def plot_pose_cube(img, yaw, pitch, roll, tdx=None, tdy=None, size=150.):
    """
    Plot a cube to the face, input is a cv2 image
    Where (tdx, tdy) is the translation of the face.
    For pose we have [pitch yaw roll tdx tdy tdz scale_factor]

    :param img:
    :param yaw:
    :param pitch:
    :param roll:
    :param tdx:
    :param tdy:
    :param size:
    :return:
    """

    p = pitch * np.pi / 180
    y = -(yaw * np.pi / 180)
    r = roll * np.pi / 180
    if tdx != None and tdy != None:
        face_x = tdx - 0.50 * size
        face_y = tdy - 0.50 * size

    else:
        height, width = img.shape[:2]
        face_x = width / 2 - 0.5 * size
        face_y = height / 2 - 0.5 * size

    x1 = size * (cos(y) * cos(r)) + face_x
    y1 = size * (cos(p) * sin(r) + cos(r) * sin(p) * sin(y)) + face_y
    x2 = size * (-cos(y) * sin(r)) + face_x
    y2 = size * (cos(p) * cos(r) - sin(p) * sin(y) * sin(r)) + face_y
    x3 = size * (sin(y)) + face_x
    y3 = size * (-cos(y) * sin(p)) + face_y

    # Draw base in red
    cv2.line(img, (int(face_x), int(face_y)), (int(x1), int(y1)), (0, 0, 255), 3)
    cv2.line(img, (int(face_x), int(face_y)), (int(x2), int(y2)), (0, 0, 255), 3)
    cv2.line(img, (int(x2), int(y2)), (int(x2 + x1 - face_x), int(y2 + y1 - face_y)), (0, 0, 255), 3)
    cv2.line(img, (int(x1), int(y1)), (int(x1 + x2 - face_x), int(y1 + y2 - face_y)), (0, 0, 255), 3)
    # Draw pillars in blue
    cv2.line(img, (int(face_x), int(face_y)), (int(x3), int(y3)), (255, 0, 0), 2)
    cv2.line(img, (int(x1), int(y1)), (int(x1 + x3 - face_x), int(y1 + y3 - face_y)), (255, 0, 0), 2)
    cv2.line(img, (int(x2), int(y2)), (int(x2 + x3 - face_x), int(y2 + y3 - face_y)), (255, 0, 0), 2)
    cv2.line(img, (int(x2 + x1 - face_x), int(y2 + y1 - face_y)),
             (int(x3 + x1 + x2 - 2 * face_x), int(y3 + y2 + y1 - 2 * face_y)), (255, 0, 0), 2)
    # Draw top in green
    cv2.line(img, (int(x3 + x1 - face_x), int(y3 + y1 - face_y)),
             (int(x3 + x1 + x2 - 2 * face_x), int(y3 + y2 + y1 - 2 * face_y)), (0, 255, 0), 2)
    cv2.line(img, (int(x2 + x3 - face_x), int(y2 + y3 - face_y)),
             (int(x3 + x1 + x2 - 2 * face_x), int(y3 + y2 + y1 - 2 * face_y)), (0, 255, 0), 2)
    cv2.line(img, (int(x3), int(y3)), (int(x3 + x1 - face_x), int(y3 + y1 - face_y)), (0, 255, 0), 2)
    cv2.line(img, (int(x3), int(y3)), (int(x3 + x2 - face_x), int(y3 + y2 - face_y)), (0, 255, 0), 2)

    return img


def plot_head_data_mov(file_direction: str, time_in_seconds: list[float], pitch_vals: list, yaw_vals: list,
                       roll_vals: list):
    """
    Plot the head movement over time in a 3d plot

    :param file_direction:
    :param time_in_seconds:
    :param pitch_vals:
    :param yaw_vals:
    :param roll_vals:
    :return:
    """
    plt.figure(figsize=(10, 8))

    off_screen_label_added = False

    plt.subplot(3, 1, 1)
    plt.plot(time_in_seconds, pitch_vals, label='Pitch')
    for i in range(len(pitch_vals)):
        if pitch_vals[i] == 0:
            plt.axvspan(time_in_seconds[i - 1], time_in_seconds[i], facecolor='red', alpha=0.3,
                        label='Off Screen' if not off_screen_label_added else "")
            off_screen_label_added = True
    plt.xlabel('Time (seconds)')
    plt.ylabel('Angle (degrees)')
    plt.legend()

    off_screen_label_added = False

    plt.subplot(3, 1, 2)
    plt.plot(time_in_seconds, yaw_vals, label='Yaw')
    for i in range(len(yaw_vals)):
        if yaw_vals[i] == 0:
            plt.axvspan(time_in_seconds[i - 1], time_in_seconds[i], facecolor='red', alpha=0.3,
                        label='Off Screen' if not off_screen_label_added else "")
            off_screen_label_added = True
    plt.xlabel('Time (seconds)')
    plt.ylabel('Angle (degrees)')
    plt.legend()

    off_screen_label_added = False

    plt.subplot(3, 1, 3)
    plt.plot(time_in_seconds, roll_vals, label='Roll')
    for i in range(len(roll_vals)):
        if roll_vals[i] == 0:
            plt.axvspan(time_in_seconds[i - 1], time_in_seconds[i], facecolor='red', alpha=0.3,
                        label='Off Screen' if not off_screen_label_added else "")
            off_screen_label_added = True
    plt.xlabel('Time (seconds)')
    plt.ylabel('Angle (degrees)')
    plt.legend()

    plt.tight_layout()
    plt.savefig(f'{file_direction}_head_movement.png')


def plot_head_data_speed(file_direction: str, time_in_seconds: np.ndarray, head_speeds_mm: np.ndarray,
                         threshold_mm: float):
    """
    Plot the head speed over time in mm/second

    :param file_direction:
    :param time_in_seconds:
    :param head_speeds_mm:
    :param threshold_mm:
    :return:
    """
    plt.figure()

    plt.plot(time_in_seconds, head_speeds_mm)
    off_screen_label_added = False

    # Checks for subject if it is not on-screen
    for i in range(len(head_speeds_mm)):
        if head_speeds_mm[i] == 0:
            plt.axvspan(time_in_seconds[i - 1], time_in_seconds[i], facecolor='red', alpha=0.3,
                        label='Off Screen' if not off_screen_label_added else "")
            off_screen_label_added = True

    plt.xlabel('Time (seconds)')
    plt.ylabel('Head Movement Speed (mm)')
    plt.title('Head Movement Speed Over Time')
    plt.axhline(y=threshold_mm, color='r', linestyle='--', label='Threshold')
    plt.legend()
    plt.savefig(f'{file_direction}_head_speed.png')


def ensure_dir_created(output_dir: str) -> None:
    """
    Util function to ensure directory has been created and if
    not then create such directory

    :param output_dir:
    :return:
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
