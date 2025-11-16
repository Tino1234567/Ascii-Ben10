import cv2
import os
import pygame
import time

# === Konversi Frame ke ASCII Berwarna ===
def frame_to_ascii(frame, width=110, height=35):
    frame = cv2.resize(frame, (width, height))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    chars = " ./:-%@,*"
    ascii_frame = ""
#  .:-=+*#%@
    for y in range(frame.shape[0]):
        for x in range(frame.shape[1]):
            pixel_gray = gray[y, x]
            b, g, r = frame[y, x]  # OpenCV pakai BGR
            char = chars[int(pixel_gray) * len(chars) // 256]
            ascii_frame += f"\033[38;2;{r};{g};{b}m{char}\033[0m"
        ascii_frame += "\n"
    return ascii_frame


# === Main Video Player Sinkron Audio ===
def play_video_ascii(video_path, audio_duration, start_time, width=120, height=35, loop=False):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    while True:
        current_time = time.time() - start_time

        # Kalau audio habis → stop
        if current_time >= audio_duration:
            break

        target_frame = int((current_time * fps) % total_frames if loop else current_time * fps)

        # Cegah keluar range
        if target_frame >= total_frames:
            break

        cap.set(cv2.CAP_PROP_POS_FRAMES, int(target_frame))
        ret, frame = cap.read()
        if not ret:
            break

        ascii_frame = frame_to_ascii(frame, width, height)
        os.system("cls" if os.name == "nt" else "clear")
        print(ascii_frame)

    cap.release()


# === Play Audio pakai pygame ===
def play_audio(audio_path):
    pygame.mixer.init()
    sound = pygame.mixer.Sound(audio_path)
    duration = sound.get_length()
    sound.play()
    return duration


# === Main Program ===
if __name__ == "__main__":
    video_path = r"C:\Users\asusn\OneDrive\Desktop\omniverse.mp4"
    audio_path = r"C:\Users\asusn\OneDrive\Desktop\omniverse.mp3"

    pygame.mixer.init()
    sound = pygame.mixer.Sound(audio_path)
    audio_duration = sound.get_length()

    start_time = time.time()
    sound.play()

    # loop=True → video bakal ulang sampai audio selesai
    play_video_ascii(video_path, audio_duration, start_time, width=120, height=35, loop=True)
