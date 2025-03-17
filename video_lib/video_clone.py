
import requests
from dotenv import load_dotenv
from moviepy.editor import VideoFileClip, concatenate_videoclips
import cv2
import os
import ffmpeg
import shutil
# Load environment variables
load_dotenv()

PEXELS_API_KEYS = os.getenv("PEXELS_API_KEY")

def get_video_duration(video_path):
    try:
        probe = ffmpeg.probe(video_path)
        duration = float(probe["format"]["duration"])  # Duration in seconds
        return duration
    except Exception as e:
        print(f"Error getting duration: {e}")
        return None

def slice_video(input_path, output_path, duration):
    clip = VideoFileClip(input_path)  # Load the video
    sliced_clip = clip.subclip(0, duration)  # Slice the first 'duration' seconds
    sliced_clip.write_videofile(output_path, codec="libx264", fps=clip.fps) 



def join_videos(video_paths, output_path="output.mp4"):
    try:
        # Load all video clips
        clips = [VideoFileClip(path) for path in video_paths]

        # Find the max width & height among all videos
        max_width = max(clip.w for clip in clips)
        max_height = max(clip.h for clip in clips)

        # Resize & pad videos to match the max dimensions
        def resize_and_pad(clip):
            return clip.resize(height=max_height).resize(width=max_width)

        resized_clips = [resize_and_pad(clip) for clip in clips]

        # Concatenate videos smoothly
        final_clip = concatenate_videoclips(resized_clips, method="compose")

        # Export merged video
        final_clip.write_videofile(output_path, codec="libx264", fps=clips[0].fps, preset="ultrafast")

        # Close resources
        for clip in clips:
            clip.close()

        print(f"✅ Successfully merged and saved as {output_path}")
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

        

def fetch_pexels_videos(query, output_path, duration, per_page=3, orientation="portrait", size="medium"):
    url = "https://api.pexels.com/videos/search"
    headers = {"Authorization": PEXELS_API_KEYS}
    params = {
        "query": query,
        "per_page": per_page,
        "orientation": orientation,
        "size": size
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        video_flag = False
        for video in data.get("videos", []):
            if video["video_files"]:
                video_url = video["video_files"][0]["link"]  # Get the first available video file
                video_id = video["id"]
                
                # Download and save the video
                video_response = requests.get(video_url, stream=True)
                if video_response.status_code == 200:
                    temp_video = output_path.replace(".mp4", "_temp.mp4")  # Temporary file
                    with open(temp_video, "wb") as file:
                        for chunk in video_response.iter_content(1024):
                            file.write(chunk)
                    
                    if get_video_duration(temp_video) > duration: 
                        # Remove audio
                        clip = VideoFileClip(temp_video).without_audio()
                        clip.write_videofile(output_path, codec="libx264", audio=False)
                        os.remove(temp_video)  # Clean up
                        video_flag = True
                        print(f"Downloaded (No Audio): {query}")
                        break
                    else:
                        print(f"Video duration is less than {duration} seconds. Skipping...")
                        os.remove(temp_video)
                else:
                    print(f"Failed to download video {video_id}")
        return video_flag
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return False


def video_creation(data,root_path,video_type='portrait'):
    sub_video = os.path.join(root_path,'sub_videos')
    if not os.path.exists(sub_video):
        os.makedirs(sub_video)
        
    object_data_filter = []
    object_len = len(data)
    object_data_filter.append((data[0][0],round(data[0][1],3),round(data[0][1],3)))
    i=1
    while i<object_len:
        object_data_filter.append((data[i][0],round(data[i][1],3),round(data[i][1]-data[i-1][1],3)))
        i+=1
    
    cropped_video = []
    for keyword,time,duration in object_data_filter:
        video_path = os.path.join(sub_video,f'{keyword}_{round(time,3)}.mp4')
        status = fetch_pexels_videos(keyword, video_path, duration, per_page=3, orientation=video_type)
        if status:
            outpath = os.path.join(sub_video,f'sliced_{keyword}_{time}.mp4')
            slice_video(video_path,outpath,duration)
            os.remove(video_path)
            cropped_video.append(outpath)
        else:
            print(f"Failed to download video for {keyword}")
            return False
    
    if cropped_video:
        final_video = os.path.join(root_path,'video_data.mp4')
        final_video_status = join_videos(cropped_video,final_video)
        if final_video_status:
            shutil.rmtree(sub_video, ignore_errors=True)
            return final_video
        else:
            return False
        

if __name__=='__main__':
    # data_set = [('talent', 6.722), ('recognition', 13.386), ('matters', 19.424), ('belief', 23)]
    data_set =  [('bookstore', 6.56), ('air', 13.015), ('symbols', 19.597), ('room', 25.983), ('Library', 31.997), ('voice', 42)]
    video_creation(data_set,'data/20250316_143140')
    
    
    