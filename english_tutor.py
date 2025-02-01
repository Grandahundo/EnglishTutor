import os
import voice
import voice_record
import streaming_asr_demo
from openai import OpenAI
import glob

client = OpenAI(
    api_key = os.environ.get("ARK_API_KEY"),
    base_url = "https://ark.cn-beijing.volces.com/api/v3",
)


background_knowledge = '''
you are a cat, you are supposed to answer in English.
when user says somthing, you are supposed to answer first, and then give some feedback on the user's grammar or vocabulary within 20 words.
the user is gonna take an IELTS test, and you are gonna help him/her to prepare for the test.
you are gonna help with grammar, vocabulary.
you can ignore capitalization and punctuation when not neccessary.
you are supposed to chat normally, and besides, at the end of each sentence, you are gonna tell the user the grammar or vocabulary mistake in the sentence.
'''

background_knowledge = '''
你是一只猫，我们要说中文.
语音输入请按v
退出请按exit
'''

SYSTEM_MESSAGE = {"role": "system", "content": background_knowledge}

# Non-streaming:
print("----- standard request -----")
history_messages = [
            SYSTEM_MESSAGE,
            # {"role": "system", "content": "you are an AI assistant developed by ByteDance, you are supposed to answer in English, here you are gonna be a cat, and you are gonna behave like a cat"},
            # {"role": "user", "content": "常见的十字花科植物有哪些？"},
        ]

index = 0
while True:
    user_message = input("User: (input v for voice input, exit to quit) ")
    if user_message == "v":
        temp_path = f"voice_input_{index}.wav"
        voice_record.start_audio(time=6, save_file=temp_path)
        user_message = streaming_asr_demo.convert_to_text(temp_path)
    if user_message == "exit":
        break
    history_messages.append({"role": "user", "content": user_message})
    completion = client.chat.completions.create(
        model = "ep-20250201092935-6lnjz",  # your model endpoint ID
        messages = history_messages,
    )
    ai_reply = completion.choices[0].message.content
    print(completion.choices[0].message.content)
    voice.say(str(ai_reply), index)
    history_messages.append({"role": "assistant", "content": completion.choices[0].message.content})
    index += 1

def remove_temp_audio_files():
    for file in glob.glob("voice_input_*.wav"):
        try:
            os.remove(file)
        except:
            pass
    for file in glob.glob("temp_audio_*.wav"):
        try:
            os.remove(file)
        except:
            pass

if input("delete temp audio files? (y/n): ") == "y":
    remove_temp_audio_files()
