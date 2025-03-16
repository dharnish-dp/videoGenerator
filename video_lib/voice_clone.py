import os
import json
import random
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import base64
import io



######################################################################################################################################################
#########################################################- Support Functions -########################################################################
######################################################################################################################################################

# Load environment variables
load_dotenv()

# Path to voice map JSON
voice_map_dir = os.path.join(os.getcwd(), "mapping", "voice_map.json")

# Function to get a random voice ID based on type
def get_random_voice(content_type):
    try:
        with open(voice_map_dir, 'r') as file:
            voice_map = json.load(file)
        
        if content_type in voice_map:
            selected_voice = random.choice(voice_map[content_type])
            return selected_voice["id"]
        else:
            print(f"❌ No voices found for type: {content_type}")
            return None
    except FileNotFoundError:
        print("❌ Voice map file not found!")
        return None
    except json.JSONDecodeError:
        print("❌ Error parsing voice map JSON!")
        return None

######################################################################################################################################################
#########################################################- Main Voice Gen Function -##################################################################
######################################################################################################################################################

# Function to generate and save voice audio
def generate_voice(text, content_type='Motivational', output_file = "test.mp3"):
    # Get a random voice ID based on content type
    voice_id = get_random_voice(content_type.lower())
    if not voice_id:
        print("⚠️ Invalid content type. Voice generation failed.")
        return False
    
    # Get API key from environment variables
    api_key = os.getenv("ELEVENLABS_API_KEY")
    
    if not api_key:
        print("❌ API key not found! Please set ELEVENLABS_API_KEY.")
        return False
    
    # Generate voice audio
    try:
        client = ElevenLabs(
            api_key=api_key,
        )
        response = client.text_to_speech.convert_with_timestamps(
                    voice_id=voice_id,
                    output_format="mp3_44100_128",
                    text=text,
                    model_id="eleven_multilingual_v2"
                )
        response_data = response.json()
        response_data = json.loads(response_data)
        audio_base64 = response_data.get('audio_base_64', '')
        
        if not audio_base64:
                print("⚠️ 'audio_base_64' key is missing or empty!")
                return False
            
        missing_padding = len(audio_base64) % 4
        if missing_padding:
                print(f"⚠️ Fixing base64 padding by adding {4 - missing_padding} characters.")
                audio_base64 += "=" * (4 - missing_padding)
                
        audio_bytes = base64.b64decode(audio_base64)
        audio_stream = io.BytesIO(audio_bytes)

        # Save the audio file in chunks
        chunk_size = 4096  # Adjust chunk size as needed

        with open(output_file, "wb") as file:
            while chunk := audio_stream.read(chunk_size):
                file.write(chunk)
                
        print(f"MP3 file saved successfully as {output_file}")
        return response_data['alignment']
    except:
        print("❌ Error generating voice audio!")
        return False

######################################################################################################################################################
#########################################################- Test Modules -#############################################################################
######################################################################################################################################################

# Test the voice generation method
if __name__ == '__main__':
    text = "Hello, this is a test"
    content_type = "Motivational"
    generate_voice(text, content_type)
