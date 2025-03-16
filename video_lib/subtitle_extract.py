import re

def generate_srt(data,path):
    characters = data["characters"]
    start_times = data["character_start_times_seconds"]
    end_times = data["character_end_times_seconds"]

    words = []
    word_start_time = None
    current_word = ""

    for i, char in enumerate(characters):
        if re.match(r'\S', char):  # If not a space, add to current word
            if current_word == "":  # New word starts
                word_start_time = start_times[i]
            current_word += char
        else:
            if current_word:  # If we had a word, store it
                words.append((current_word, word_start_time, end_times[i-1]))
                current_word = ""

    if current_word:  # Capture the last word
        words.append((current_word, word_start_time, end_times[-1]))

    # Generate SRT format
    srt_data = ""
    for idx, (word, start, end) in enumerate(words, 1):
        srt_data += f"{idx}\n{format_time(start)} --> {format_time(end)}\n{word}\n\n"
    with open(path, "w", encoding="utf-8") as file:
        file.write(srt_data)

    return words

def format_time(seconds):
    """Convert seconds to SRT time format (HH:MM:SS,MS)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    sec = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{sec:02},{millis:03}"

if __name__ == '__main__':
    data = {
        "characters": ["H","e","l","l","o",","," ","t","h","i","s"," ","i","s"," ","a"," ","t","e","s","t"],
        "character_start_times_seconds": [0.0,0.197,0.267,0.302,0.372,0.488,0.557,0.592,0.615,0.662,0.697,0.731,0.778,0.824,0.859,0.906,0.94,0.987,1.045,1.173,1.242],
        "character_end_times_seconds": [0.197,0.267,0.302,0.372,0.488,0.557,0.592,0.615,0.662,0.697,0.731,0.778,0.824,0.859,0.906,0.94,0.987,1.045,1.173,1.242,1.625]
    }

    srt_content = generate_srt(data)
    with open("output.srt", "w", encoding="utf-8") as file:
        file.write(srt_content)
    print("SRT file generated: output.srt")
