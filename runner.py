from video_lib.video_maker import VideoMaker
import os
import json

if __name__=="__main__":
    
    # Read data from config file
    config_json_path = os.path.join(os.getcwd(),"config.json")
    with open(config_json_path,'r') as config_file:
        config = json.load(config_file)

    text = config.get('input text','')
    post = config.get('post','')
    output_folder = config.get('output folder','data')
    video_type = config.get('video type','portrait')
    content_type = config.get('content type','storytelling')
    watermark = config.get('watermark',False)
    
    
    # Create Video Using Config file
    video_maker_obj = VideoMaker(text,video_type,content_type,watermark,output_folder)
    status = video_maker_obj.video_generate()  
    
    
    
            
    