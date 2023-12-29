import asyncio
import os
import pickle
import threading
import time
import argparse

import pyautogui

from src.control_capture.capture_control import MouseListener, KeyboardListener

parser = argparse.ArgumentParser()
parser.add_argument("run_id", default="test", type=str, help="The run id to use for saving the data")
parser.add_argument("--data_save_path", default="./data", type=str, help="The path to save the data")
args = parser.parse_args()

RUN_ID = args.run_id
DATA_SAVE_PATH = args.data_save_path


async def save_file_async(fname, events_data_copy, overwrite=False):
    if not overwrite and os.path.exists(fname):
        print(f"File already exists: {fname}")

    pickle.dump(events_data_copy, open(fname, "wb"))


async def main():
    mouse_listener = MouseListener(filepath=os.path.join(DATA_SAVE_PATH, f"{RUN_ID}_mouse.txt"))
    keyboard_listener = KeyboardListener(filepath=os.path.join(DATA_SAVE_PATH, f"{RUN_ID}_keyboard.txt"))
    mouse_listener.start()
    keyboard_listener.start()

    background_tasks = []

    try:
        video_counter = 0
        while True:
            ims = []
            for j in range(200):
                img = pyautogui.screenshot()
                t0 = time.time()
                img = img.resize((960, 540))
                print(f"Screenshot took {time.time() - t0} seconds")
                ims.append({"timestamp": time.time(), "data": img})
            print(f"Saving {len(ims)} images")

            ev_loop = asyncio.new_event_loop()
            task = ev_loop.create_task(save_file_async(os.path.join(DATA_SAVE_PATH,f"{RUN_ID}_video_{video_counter}.pkl"), ims.copy()))
            thread = threading.Thread(target=ev_loop.run_until_complete, args=[task])

            video_counter += 1
            mouse_listener.save()
            keyboard_listener.save()

            # Start the thread
            background_tasks.append(thread)
            thread.start()
    except KeyboardInterrupt:
        print("Stopping...")


    # Wait for all the threads to complete
    for thread in background_tasks:
        thread.join()

    mouse_listener.stop()
    keyboard_listener.stop()


asyncio.run(main())
