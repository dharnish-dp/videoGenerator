import ffmpeg
import os

def merge_video_audio(video_path, audio_path, output_path="output_with_audio.mp4"):
    try:
        # Get video duration using ffmpeg
        probe = ffmpeg.probe(video_path)
        video_duration = float(next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')['duration'])

        # Apply audio trimming to match the video duration
        input_audio = ffmpeg.input(audio_path).filter('atrim', duration=video_duration)

        # Load video
        input_video = ffmpeg.input(video_path)

        # Merge video and trimmed audio
        ffmpeg.output(input_video, input_audio, output_path, vcodec='copy', acodec='aac', strict='experimental').run(overwrite_output=True)

        print(f"✅ Merged video saved as {output_path}")
        
    
    except Exception as e:
        print(f"❌ Error: {e}") 

def apply_overlay_and_subtitles(video_path, srt_path, output_path="final_output_video.mp4"):
    try:
        # Define FFmpeg input
        input_video = ffmpeg.input(video_path)

        # Apply slight black overlay & centered subtitles
        filtered_video = (
            input_video.video
            .filter("drawbox", color="black@0.1", width="iw", height="ih", thickness="fill")  # Slight dark overlay
            .filter("subtitles", srt_path, force_style="Alignment=10,FontName=Arial,FontSize=24,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,BorderStyle=1,Outline=2,Shadow=2,MarginV=20")
        )

        # Extract audio if available
        try:
            input_audio = input_video.audio
            output = ffmpeg.output(filtered_video, input_audio, output_path, vcodec="libx264", acodec="aac", strict="experimental")
        except ffmpeg.Error:
            print("⚠️ No audio stream found in the video. Proceeding without audio.")
            output = ffmpeg.output(filtered_video, output_path, vcodec="libx264")

        # Run the FFmpeg command
        output.run(overwrite_output=True)

        print(f"✅ Styled subtitles, overlay, and audio applied: {output_path}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__=="__main__":
    video_path = 'data/20250314_210036/final_video.mp4'
    voice_path = 'data/20250314_210036/voice.mp3'
    srt_path = 'data/20250314_210036/voice.srt'
    
    output_production_video = 'data/20250314_210036/production_video.mp4'
    merge_video_audio(video_path, voice_path,    output_production_video)  # default output is output_with_audio.mp4
    
    output_video_with_subtitle = 'data/20250314_210036/final_video_with_subtitles.mp4'
    apply_overlay_and_subtitles(output_production_video,srt_path,output_video_with_subtitle)
    
    final_output_video = 'data/20250314_210036/production.mp4'
    merge_video_audio(output_video_with_subtitle, voice_path,    final_output_video)
    
    os.remove(output_production_video)
    os.remove(output_video_with_subtitle)  