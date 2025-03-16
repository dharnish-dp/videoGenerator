#######################################################################################################################################################################################
########################################################- Basic Import -###############################################################################################################
#######################################################################################################################################################################################

import os
import datetime
from .voice_clone import *
from .subtitle_extract import *
from .object_extract import *
from .video_clone import *
from .merge_data import *

#######################################################################################################################################################################################
########################################################- Main Class -#################################################################################################################
#######################################################################################################################################################################################

class VideoMaker:
    def __init__(self, input_text,video_type,content_type,watermark,output_folder):
        self.input_text = input_text
        self.video_type = video_type
        self.content_type = content_type
        self.watermark = watermark
        self.output_folder = output_folder
        self.process_code = ""
        self.process_path = ""
        self.voice_path = ""
    
    
    def video_generate(self):
        self.process_path = self.make_dir()
        if self.process_path:
            print("preparing voice data")
            self.voice_path = os.path.join(self.process_path,"voice.mp3")
            subtitle_data = generate_voice(self.input_text,content_type=self.content_type,output_file=self.voice_path)
            if subtitle_data:
                str_path = os.path.join(self.process_path,"voice.srt")
                word_level_time_stamp = generate_srt(subtitle_data,str_path)
                object_timestamp = get_keyword_timestamp(word_level_time_stamp)
                if object_timestamp:
                    video_path = video_creation(object_timestamp,self.process_path,self.video_type)
                    if video_path:
                        audio_merge = os.path.join(self.process_path,'audio_merge.mp4')
                        merge_video_audio(video_path,self.voice_path,audio_merge)
                        subitile_merge = os.path.join(self.process_path,'subtitle_merge.mp4')
                        apply_overlay_and_subtitles(audio_merge,str_path,subitile_merge)
                        final_video = os.path.join(self.process_path,'video.mp4')
                        merge_video_audio(subitile_merge,self.voice_path,final_video)   
                        os.remove(audio_merge)
                        os.remove(subitile_merge)
                        os.remove(video_path)
                    else:
                        print("Video Creation Failed")            
                else:
                    print("\nError: No Object timestamp found.")
            else:
                print("\nError in generating voice")
        else:
            print("\nError: Unable to create process folder")
                
                
                
    def make_dir(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        for i in range(10):
            self.process_code = self.generate_folder_with_timestamp()
            if self.process_code not in self.get_folders(self.output_folder):
                break
        process_path = os.path.join(self.output_folder,self.process_code)
        os.makedirs(process_path)
        return process_path
    
        
    def generate_folder_with_timestamp(base_path="output"):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return timestamp
    
    
    def get_folders(self,output_folder):
        return [f for f in os.listdir(output_folder) if os.path.isdir(os.path.join(output_folder, f))]