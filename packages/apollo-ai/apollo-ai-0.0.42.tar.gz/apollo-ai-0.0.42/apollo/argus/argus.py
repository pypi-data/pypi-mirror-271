import cv2
import mediapipe as mp
from sixdrepnet import SixDRepNet
from face_detection import RetinaFace
from scipy.spatial import distance
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import numpy as np
import time
import logging
import math
from .utils import (
    plot_pose_cube,
    filter_video_data,
    plot_head_data_mov,
    plot_head_data_speed
)
from .utils import ensure_dir_created

logging.basicConfig(format='APOLLO: (%(asctime)s): %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p',
                    level=logging.DEBUG)


def mouth_movement(filepath: str, focal_length_mm: int, output_dir='./output', plot=False,
                   normalize=False, lim: list[float, float] = None) -> dict:
    """
    Generates the face data points for a given video, it currently accepts a small variety of part indices in the face

    :param filepath:
    :param focal_length_mm:
    :param output_dir:
    :param plot:
    :param normalize:
    :param lim:
    :return:
    """
    ensure_dir_created(output_dir)

    file_direction = output_dir + "/" + filepath.split("/")[-1].split(".")[0]

    distances_data = []

    video_source = cv2.VideoCapture(filepath)
    logging.info("Video found, starting processing...")
    mp_face_dots = mp.solutions.face_mesh

    fps_general = int(video_source.get(cv2.CAP_PROP_FPS))
    frame_width = int(video_source.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_source.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(video_source.get(cv2.CAP_PROP_FRAME_COUNT))

    start_frame, end_frame = 0, total_frames

    # Check if the limits are correctly set if defined
    if lim is not None:
        start_frame, end_frame = [int(x * fps_general) for x in lim]
        if start_frame < 0 or end_frame > total_frames:
            raise ValueError("The time limits do not match with the length of the video")

    # Codec and VideoWriter object to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    out = cv2.VideoWriter(f'{file_direction}_face_points.mp4', fourcc, fps_general,
                          (frame_width, frame_height))

    # Mediapipe face landmark with 468 points
    face_mesh = mp_face_dots.FaceMesh(min_detection_confidence=0.5)

    max_distance = 0  # Initialize the maximum observed distance
    min_distance = float('inf')  # Initialize the minimum observed distance

    frame_counter = 0

    while video_source.isOpened():
        ret, frame = video_source.read()

        # If not more frames are found stop the recognition
        if not ret or frame is None:
            break

        # Skip frames outside limits
        if lim is not None and (frame_counter < start_frame or frame_counter > end_frame):
            frame_counter += 1
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results_facial_dots = face_mesh.process(rgb_frame)

        fh, fw, _ = frame.shape

        if results_facial_dots.multi_face_landmarks:
            # Only select the points 0 and 17
            index_top, index_bottom, mp_face_part = 0, 17, mp_face_dots.FACEMESH_LIPS

            for source_idx, _ in mp_face_part:
                source = results_facial_dots.multi_face_landmarks[0].landmark[source_idx]
                x = int(source.x * fw)
                y = int(source.y * fh)

                source_top = results_facial_dots.multi_face_landmarks[0].landmark[index_top]
                x_top = int(source_top.x * fw)
                y_top = int(source_top.y * fh)

                source_bottom = results_facial_dots.multi_face_landmarks[0].landmark[index_bottom]
                x_bottom = int(source_bottom.x * fw)
                y_bottom = int(source_bottom.y * fh)

                # Applying chebyshev distance
                distance_px = int(distance.chebyshev([x_top, y_top], [x_bottom, y_bottom]))
                distance_mm = int(
                    (distance_px * focal_length_mm) / (focal_length_mm * 2 * math.tan(math.radians(0.5))))
                timestamp = video_source.get(cv2.CAP_PROP_POS_MSEC)
                distances_data.append([(distance_mm / 100), timestamp / 1000])

                cv2.circle(frame, (x, y), 2, (255, 255, 255), -1)

                max_distance = max(max_distance, distance_mm / 100)
                min_distance = min(min_distance, distance_mm / 100)

        out.write(frame)  # Write the frame to the output video file
        frame_counter += 1

    video_source.release()
    cv2.destroyAllWindows()

    distances_data = filter_video_data(distances_data, normalize)
    x_values = distances_data['Timestamp'].tolist()
    y_values = distances_data['Distance'].tolist()

    data = {"x_values": x_values, "y_values": y_values, "fps": fps_general, "min_distance": min_distance,
            "max_distance": max_distance, "frame_width": frame_width, "frame_height": frame_height}

    if plot:
        # Middle line value to specify the mouth closing region
        threshold = ((max_distance + min_distance) / 2) * 0.6

        plt.figure(figsize=(10, 6))
        plt.plot(x_values, y_values, label="Part Opening Distance", color='b')
        plt.xlabel("Timestamp (s)")
        plt.ylabel("Distance (mm)")
        plt.title("Distance vs. Timestamp")
        plt.axhline(y=threshold, color='r', linestyle='--', label='Threshold')
        plt.grid(True)
        plt.legend()
        plt.savefig(f'{file_direction}.png')

    return data


def head_position(filepath: str, output_dir="./output", plot=False, real_head_width=145,
                  lim: list[float, float] = None) -> dict:
    """
    Estimates the head position over time

    :param filepath:
    :param output_dir:
    :param plot:
    :param real_head_width:
    :param lim:
    :return:
    """
    ensure_dir_created(output_dir)

    file_direction = output_dir + "/" + filepath.split("/")[-1].split(".")[0]

    model = SixDRepNet()
    detector = RetinaFace()

    video_source = cv2.VideoCapture(filepath)
    logging.info("Video found, starting processing...")

    fps_general = int(video_source.get(cv2.CAP_PROP_FPS))
    frame_width = int(video_source.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_source.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(video_source.get(cv2.CAP_PROP_FRAME_COUNT))

    start_frame, end_frame = 0, total_frames

    # Check if the limits are correctly set if defined
    if lim is not None:
        start_frame, end_frame = [int(x * fps_general) for x in lim]
        if start_frame < 0 or end_frame > total_frames:
            raise ValueError("The time limits do not match with the length of the video")

    # Codec and VideoWriter object to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    out = cv2.VideoWriter(f'{file_direction}_head_position.mp4', fourcc,
                          fps_general,
                          (frame_width, frame_height))

    prev_time = None
    prev_head_pos = None
    head_movement_speeds = []
    yaws = []
    pitchs = []
    rolls = []

    start_time = time.time()
    frame_counter = 0
    bbox_width = 0

    while video_source.isOpened():
        ret, frame = video_source.read()

        # If not more frames are found stop the recognition
        if not ret or frame is None:
            break

        # Skip frames outside limits
        if lim is not None and (frame_counter < start_frame or frame_counter > end_frame):
            frame_counter += 1
            continue

        faces = detector(frame)

        if len(faces) == 0:
            # No faces detected, add zeros
            yaws.append(0)
            pitchs.append(0)
            rolls.append(0)
            head_movement_speeds.append(0)
            continue

        for box, landmarks, score in faces:
            if score < .95:
                continue
            x_min = int(box[0])
            y_min = int(box[1])
            x_max = int(box[2])
            y_max = int(box[3])
            bbox_width = abs(x_max - x_min)
            bbox_height = abs(y_max - y_min)

            x_min = max(0, x_min - int(0.2 * bbox_height))
            y_min = max(0, y_min - int(0.2 * bbox_width))
            x_max = x_max + int(0.2 * bbox_height)
            y_max = y_max + int(0.2 * bbox_width)

            if x_min >= x_max or y_min >= y_max:
                logging.error("Invalid bounding box coordinates")
                continue

            img = frame[y_min:y_max, x_min:x_max]

            if frame.size == 0:
                logging.error("Empty image slice")
                continue

            pitch, yaw, roll = model.predict(img)

            if isinstance(pitch, (list, np.ndarray)):
                pitch = pitch[0]
            if isinstance(yaw, (list, np.ndarray)):
                yaw = yaw[0]
            if isinstance(roll, (list, np.ndarray)):
                roll = roll[0]

            yaws.append(yaw)
            pitchs.append(pitch)
            rolls.append(roll)

            curr_time = time.time()
            curr_head_pos = np.array([pitch, yaw, roll])
            if prev_head_pos is not None:
                head_movement = np.linalg.norm(curr_head_pos - prev_head_pos)
                time_elapsed = curr_time - prev_time
                head_movement_speed = head_movement / time_elapsed
                head_movement_speeds.append(head_movement_speed)

            prev_time = curr_time
            prev_head_pos = curr_head_pos

            frame = plot_pose_cube(frame, yaw, pitch, roll, x_min + int(.5 * (
                    x_max - x_min)), y_min + int(.5 * (y_max - y_min)), size=bbox_width)

        logging.info(f"Reading frame {frame_counter + 1}/{total_frames}")
        out.write(frame)
        frame_counter += 1

    logging.info(f"Time taken: {time.time() - start_time}")
    video_source.release()
    cv2.destroyAllWindows()

    # Formula to scale the real head with
    time_in_seconds = [frame_num / fps_general for frame_num in range(len(head_movement_speeds))]
    scale_factor = real_head_width / bbox_width

    head_speeds_mm_per_sec = [speed * scale_factor for speed in head_movement_speeds]

    # Calculate the average movement (this value can be compared to normal movement people)
    non_zero_speeds = [speed for speed in head_speeds_mm_per_sec if speed != 0]
    mean_speed = np.mean(non_zero_speeds)
    std_speed = np.std(non_zero_speeds)
    threshold = mean_speed + 2 * std_speed
    threshold_mm = threshold * scale_factor

    # Export x and y values for API (pitch, yaw, and roll values)
    min_length = min(len(time_in_seconds), len(pitchs), len(yaws), len(rolls))
    time_in_seconds = time_in_seconds[:min_length]
    pitch_vals = pitchs[:min_length]
    yaw_vals = yaws[:min_length]
    roll_vals = rolls[:min_length]

    # Export x and y values for API (head speed)
    x_head_speed = np.linspace(min(time_in_seconds), max(time_in_seconds), len(time_in_seconds))
    head_speeds_smooth = savgol_filter(head_speeds_mm_per_sec, 10, 3)  # Smooth with filter

    if plot:
        plot_head_data_mov(file_direction=file_direction,
                           time_in_seconds=time_in_seconds,
                           pitch_vals=pitch_vals,
                           yaw_vals=yaw_vals,
                           roll_vals=roll_vals)

        plot_head_data_speed(file_direction=file_direction,
                             time_in_seconds=x_head_speed,
                             head_speeds_mm=head_speeds_smooth,
                             threshold_mm=threshold_mm)

    return {"x_head_speed": x_head_speed,
            "y_head_speed": head_speeds_smooth,
            "x_head_movement": time_in_seconds,
            "y_pitch_values": pitch_vals,
            "y_yaw_values": yaw_vals,
            "y_roll_values": roll_vals,
            "threshold_speed": threshold_mm,
            "average_speed": mean_speed}

