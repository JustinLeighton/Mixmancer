import mss
import time
from PIL import Image
from PIL.Image import Image as ImageType
import threading
import pyautogui
from pathlib import Path


def capture_screen_segment(top: int, left: int, width: int, height: int, output_dir: Path):
    with mss.mss() as sct:
        # Define the region of the screen to capture
        monitor = {"top": top, "left": left, "width": width, "height": height}

        frame_count = 0
        start_time = time.time()
        elapsed_time = 0
        duration = 1.5  # Capture duration in seconds

        def save_image(sct_img: ImageType, frame_count: int):
            # Convert to PIL Image for saving
            img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)  # type: ignore
            img.save(f"{output_dir}/frame_{frame_count:04d}.png")

        while elapsed_time < duration:
            # Capture the screen
            sct_img = sct.grab(monitor)

            # Save the image in a separate thread
            threading.Thread(target=save_image, args=(sct_img, frame_count)).start()

            frame_count += 1

            # Sleep to maintain 30 frames per second
            elapsed_time = time.time() - start_time
            sleep_time = (frame_count / 30) - elapsed_time
            if sleep_time > 0:
                time.sleep(sleep_time)

        print(f"Frames: {frame_count}, Time Elapsed: {elapsed_time:.2f}s, FPS: {frame_count / elapsed_time:.2f}")


# Example usage
current_position = pyautogui.position()
pyautogui.click(current_position)
capture_screen_segment(top=177, left=0, width=1920, height=1333 - 177, output_dir=Path("assets/dice/tmp"))
