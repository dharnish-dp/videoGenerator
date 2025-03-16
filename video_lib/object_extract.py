import spacy
from math import ceil
nlp = spacy.load("en_core_web_sm")

# Convert word level time stamp to sentence time stamp
def form_sentence(word_timestamp_data):
    total_world_len = len(word_timestamp_data)
    total_duration = ceil(word_timestamp_data[-1][2])
    
    if total_world_len == 0:
        return []
    if total_duration <=10:
        sentence = ''
        end_time = ''
        for word,s_time,e_time in word_timestamp_data:
            sentence+=word
            end_time = e_time
        return [(sentence,end_time)]
    else:
        sentence_timestamp = []
        i=0
        j=0
        sentence = ''
        while i<total_world_len:
            if word_timestamp_data[i][2]-word_timestamp_data[j][2]>6:
                sentence_timestamp.append([sentence,word_timestamp_data[i][2]])
                j = i
                sentence = ''
                continue
            sentence+=word_timestamp_data[i][0]+" "
            i+=1
        if total_duration-word_timestamp_data[j][2]>3.5:
            sentence_timestamp.append([sentence,total_duration])
        else:
            sentence_timestamp[-1][0] = sentence_timestamp[-1][0]+ " " + sentence
            sentence_timestamp[-1][1] = total_duration
        
        return sentence_timestamp
    
# Extract the keyword from the sentence
def get_keyword_timestamp(word_timestamp_data):
    object_time_stamp = []
    sentence_timestamp = form_sentence(word_timestamp_data)  # Function that segments timestamps into sentences

    print("\n\nSentence Timestamps:\n", sentence_timestamp)  # Debugging output

    if sentence_timestamp:
        for i, (sentence, time) in enumerate(sentence_timestamp):
            doc = nlp(sentence)
            found = False  # Track if a word is found
            
            for token in doc:
                if token.dep_ == "dobj" and token.pos_ != "PRON":
                    object_time_stamp.append((token.text, time))
                    found = True
                    break  

            # Fallback: If no direct object is found, pick a noun
            if not found:
                for token in doc:
                    if token.pos_ == "NOUN":
                        object_time_stamp.append((token.text, time))
                        break  

    print("\n\nExtracted Objects with Timestamps:\n", object_time_stamp)
    return object_time_stamp  
                        
        




if __name__=="__main__":
    data_set = [('Liam,', 0.0, 0.464), ('a', 0.499, 0.569), ('struggling', 0.65, 1.091), ('artist,', 1.149, 1.683), 
            ('doubted', 1.765, 2.148), ('his', 2.206, 2.31), ('talent.', 2.357, 2.949), ('One', 3.46, 3.669), 
            ('day,', 3.704, 3.959), ('a', 3.982, 4.029), ('stranger', 4.11, 4.516), ('bought', 4.574, 4.818), 
            ('his', 4.853, 4.946), ('painting,', 5.004, 5.492), ('praising', 5.573, 5.979), ('its', 6.026, 6.165), 
            ('depth.', 6.211, 6.722), ('Inspired,', 7.163, 7.848), ('he', 7.872, 7.93), ('kept', 7.988, 8.197), 
            ('creating,', 8.255, 8.916), ('gaining', 9.033, 9.392), ('recognition', 9.474, 10.054), ('over', 10.124, 10.321), 
            ('time.', 10.379, 10.937), ('His', 11.447, 11.61), ('passion', 11.668, 12.028), ('turned', 12.086, 12.365), 
            ('into', 12.399, 12.574), ('success,', 12.632, 13.386), ('proving', 13.665, 14.048), ('perseverance', 14.129, 14.861), 
            ('matters.', 14.907, 15.558), ('Years', 16.254, 16.579), ('later,', 16.649, 16.986), ('he', 17.02, 17.079), 
            ('encouraged', 17.137, 17.671), ('young', 17.717, 17.88), ('artists,', 17.949, 18.611), ('reminding', 18.785, 19.25), 
            ('them', 19.296, 19.424), ('that', 19.47, 19.598), ('belief', 19.644, 19.981), ('and', 20.039, 20.144), 
            ('persistence', 20.202, 20.898), ('shape', 20.991, 21.328), ('destiny.', 21.374, 22.291)]
    get_keyword_timestamp(data_set)