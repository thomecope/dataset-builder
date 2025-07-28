import cv2
import os

"""
Extract stills and save to output_folder
"""

def extract_frames(video_path: str, output_folder: str, frame_interval:int =1, start_frame:int =0, end_frame:int =None, total_frames:int=None, short_name:str=None):
    """Extract frames from a video

    Args:
        video_path (str): path/to/video
        output_folder (str): path/to/save/imgs. will create if doesn't exist.
        frame_interval (int, optional): relative sampling rate. Defaults to 1.
        start_frame (int, optional): beginning frame. Defaults to 0.
        end_frame (int, optional): end frame. Defaults to last frame in the video.
        total_frames (int, optional): total number of frames to save. Defaults to None.
        short_name (str, optional): prefix to add to frames saved. Defaults to video name.

    Raises:
        RuntimeError: if the video doesn't load properly
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    print(f"Saving images to {output_folder}")
        
    if short_name is None:
        short_name =(os.path.basename(video_path)).split('.')[0]

    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    frames_in_video = int(video.get(cv2.CAP_PROP_FRAME_COUNT)) 
    
    print(f"Total frames = {frames_in_video}, Frames/s = {fps}")  
    
    print(f"    effective sampling rate = {fps/frame_interval:.2f} FPS")
    
    if end_frame is None or end_frame > frames_in_video:
        end_frame = frames_in_video
        print(f"    end frame set to {end_frame} ({round(end_frame/frames_in_video * 100)}%)")
    
    if total_frames is None or total_frames > frames_in_video:
        total_frames = end_frame-start_frame
        print(f"    end frame set to {total_frames} ({round(total_frames/frames_in_video * 100)}%)")
    

    frame_count = 0
    frames_saved = 0

    while True:
        
        success, frame = video.read()
        if not success:
            raise RuntimeError("video not read")
        
        if start_frame <= frame_count <= end_frame:
            if frame_count % frame_interval == 0:
                frame_filename = os.path.join(output_folder, f"{short_name}_{frame_count:06d}.jpg")
                cv2.imwrite(frame_filename, frame)
                frames_saved += 1
        
        if (frame_count >= end_frame) or (frames_saved >= total_frames):
            break
        
        frame_count += 1

    video.release()

    print(f"Extracted {frame_count // frame_interval} frames from {start_frame} to {end_frame}")


if __name__ == "__main__":
    video_path = "100fly.mp4"
    output_folder = "data/stills/100fly"
    extract_frames(video_path, output_folder, frame_interval=100, total_frames=15)