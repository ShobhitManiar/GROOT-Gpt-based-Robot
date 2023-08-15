import openai
import asyncio
import nest_asyncio
import argparse
import recorder as r
from djitellopy import Tello
import time
import re
import sys
nest_asyncio.apply()

openai.api_key = "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"  # Set the OpenAI API key

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--tprompt", type=str, default=r"D:\Thesis\tello_prompt.txt")
parser.add_argument("--tsysprompt", type=str, default=r"D:\Thesis\system_prompts.txt")
parser.add_argument("--stt", type=str, default=r"D:\Thesis\transcriptions_transcript_1.txt") # Parse another command-line argument for the speech-to-text transcript file
args = parser.parse_args()
tello=Tello()
tello.connect()

# Read system prompts and game instructions from files
with open(args.tsysprompt, "r",encoding="utf-8") as f:
    sysprompt = f.read()

with open(args.tprompt, "r", encoding="utf-8") as f:
     prompt = f.read()


# Initialize chat history with system prompt
chat_history = [
    {
        "role": "system",
        "content": sysprompt
    }]

def ask(prompt):
    chat_history.append(
        {
            "role": "user",
            "content": prompt,
        }
    )
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_history,
        temperature=0
    )
    chat_history.append(
        {
            "role": "assistant",
            "content": completion.choices[0].message.content,
        }
    )
    return chat_history[-1]["content"] 

code_block_regex = re.compile(r"'''(.*?)'''", re.DOTALL)
def extract_python_code(content):
        code_blocks = code_block_regex.findall(content)
        if code_blocks:
            full_code = "\n".join(code_blocks)
            return full_code
        
ask(prompt)  # Start the conversation by asking the initial prompt

# Function to generate GPT-3 response using the provided prompts
def GPT(prompts):
    question = str(prompts) # input()
    response = ask(question)
    print(response)  
    print(extract_python_code(response))
    print("Please wait while I run the code ....")
    #exec(extract_python_code(response))   
    print("Done!\n")

last_occurrence = -1
COMMAND_WORD="whisper"
# Function to check the transcript periodically            
async def check_transcript():
            
    global last_occurrence
    with open(args.stt,"r",encoding="utf-8") as f:
        text = f.read()
        occurrence= text.lower().rfind(COMMAND_WORD)
        if occurrence != last_occurrence:

            # get command starting at occurrence of command word
            command = text[occurrence:]
            if command.endswith("."):
                command=command[:-1]
           
            # store last occurrence so we don't repeat the same command
            last_occurrence = occurrence

            # Generate GPT response based on the command as a prompt
            global prompt 
            print("ready")
            prompts= f"""{command}""" #input()  #
            if prompts.strip().lower() == "whisper exit" or prompts.strip().lower() == "whisper, exit":
                print("Exiting the program...")
                sys.exit(0)
            else:
                GPT(prompts)
        
    time.sleep(1)
    tello.send_rc_control(0,0,0,0)


# Function to run the check_transcript() function periodically
async def run_periodically(interval, periodic_function):
    while True:
        print("say something using command word Whisper")
        r.STT()
        await asyncio.gather(asyncio.sleep(interval), periodic_function())

# Run the check_transcript() function periodically every 1 second
asyncio.run(run_periodically(1, check_transcript))

