import asyncio

import board, time,sys, supervisor
import audiobusio
import synthio
import audiomixer
import drums



import displayio
import terminalio
from adafruit_display_text import label
from adafruit_displayio_layout.layouts.grid_layout import GridLayout
from adafruit_display_shapes.circle import Circle




mix_vol = 0.2 # Mixer Volume


debug_enabled = False
# Display Setup

def dPrint(msg):
    if debug_enabled == True:
        print(msg)

display = board.DISPLAY
# Make the display context
main_group = displayio.Group()
display.root_group = main_group

h = 135
w = 240

# Input Map

input_map = {
    "e": [0,0],
    "r": [0,1],
    "t": [0,2],
    "y": [0,3],
    "u": [0,4],
    "i": [0,5],
    "o": [0,6],
    "p": [0,7],
    "s": [1,0],
    "d": [1,1],
    "f": [1,2],
    "g": [1,3],
    "h": [1,4],
    "j": [1,5],
    "k": [1,6],
    "l": [1,7],
    "z": [2,0],
    "x": [2,1],
    "c": [2,2],
    "v": [2,3],
    "b": [2,4],
    "n": [2,5],
    "m": [2,6],
    ",": [2,7]
    }



# Audio Config

audio = audiobusio.I2SOut(bit_clock=board.I2S_BIT_CLOCK, word_select=board.I2S_WORD_SELECT, data=board.I2S_DATA)

samp_rate = 24000

mixer  = audiomixer.Mixer(
                voice_count=3,
                channel_count=1,
                sample_rate=samp_rate,
                buffer_size=1024*4)

synth  = synthio.Synthesizer(
                channel_count=1,
                sample_rate=samp_rate)

synth1 = synthio.Synthesizer(
                channel_count=1,
                sample_rate=samp_rate)

synth2 = synthio.Synthesizer(
                channel_count=1,
                sample_rate=samp_rate)



# Start playing the mixer channels
audio.play(mixer)



# Add Synths to Mixer and set Volume
mixer.voice[0].play(synth)
mixer.voice[1].play(synth1)
mixer.voice[2].play(synth2)



mixer.voice[0].level = mix_vol
mixer.voice[1].level = mix_vol
mixer.voice[2].level = mix_vol

snare = drums.Snare(synth)
kick = drums.KickDrum(synth1)
hh = drums.HighHat(synth2)


bpm = 240	
delVal = 60/bpm

seq = [
        [0,0,0,0,0,0,0,0], # Snare
        [0,0,0,0,0,0,0,0], # Hi Hat
        [0,0,0,0,0,0,0,0]  # Kick Drum
    ]
     

inst_count = len(seq)
seq_count = len(seq[inst_count-1])

seq_len = seq_count
num_sounds = inst_count


# UI Definition

# layout = GridLayout(
#     x=0,
#     y=0,
#     width=220,
#     height=105,
#     grid_size=(seq_count, inst_count),
#     cell_padding=10,
# )


def updateUI():
    layout = GridLayout(
        x=0,
        y=0,
        width=220,
        height=105,
        grid_size=(seq_count, inst_count),
        cell_padding=10,
    )
    for x in range(seq_count):
        for y in range(inst_count):
    #         _labels.append(label.Label(terminalio.FONT, scale=2, x=0, y=0, text=str(seq[x][y])))
            
            layout.add_content(
                display_beat(seq[y][x]),
    #             label.Label(terminalio.FONT, scale=2, x=0, y=0, text=str(seq[y][x])),
                grid_position=(x, y),
                cell_size=(1, 1))
    return layout                





# Create array to hold labels requiring display
_labels = []



def display_beat(beat_value):
    if beat_value ==1:
        return Circle(0,0,10,fill=0xFF0000)
    else:
        return Circle(0,0,10,outline=0xFF0000)



# for x in range(seq_count):
#     for y in range(inst_count):
# #         _labels.append(label.Label(terminalio.FONT, scale=2, x=0, y=0, text=str(seq[x][y])))
#         
#         layout.add_content(
#             display_beat(seq[y][x]),
# #             label.Label(terminalio.FONT, scale=2, x=0, y=0, text=str(seq[y][x])),
#             grid_position=(x, y),
#             cell_size=(1, 1))
                






async def playSnare(v):   
    snare.play()

    
async def playKick(v):   
    kick.play()

    
async def playHat(v):
    hh.play()


scount = 0
snareTask = 0
hhTask= 0
kickTask = 0

def adjust_volume(vol_inc):
    global mix_vol
    
    mix_vol += vol_inc
    if mix_vol >= 1:
        mix_vol = 1
    elif mix_vol <= 0:
        mix_vol = 0
#     vol = Nvol
    mixer.voice[0].level = mix_vol
    mixer.voice[1].level = mix_vol
    mixer.voice[2].level = mix_vol


async def handle_kbInput():
    kbIn = ""
    if supervisor.runtime.serial_bytes_available:
        kbIn = sys.stdin.read(1)
#             print(seq[input_map[kbIn]])
#             print(str(input_map[kbIn]))
        letr = str(kbIn)
#             print(kbIn)
#         dPrint(str(kbIn))
        if letr in input_map:
            map_val = input_map[letr]
#                 beat = seq[map_val[0]][map_val[1]]
#             dPrint(seq[map_val[0]][map_val[1]])
            seq[map_val[0]][map_val[1]] = 1 - seq[map_val[0]][map_val[1]]
#             dPrint(seq[map_val[0]][map_val[1]])
            main_group.append(updateUI())
            main_group.remove(main_group[0])
#                 print(map_val[0])
#             dPrint(seq[map_val[0]][map_val[1]])
        else:
            if kbIn == ";":
                adjust_volume(0.05)
            elif kbIn == ".":
                adjust_volume(-0.05)
#                     mix_vol -= .05
#                     dPrint(mix_vol)    
#             dPrint("Unbound Key")


# def seq_Step():
async def seq_Step():
    global sCount
#     print(global mix_vol)
#     sCount = 0
#     while True:
        
        #####
        # Handle Sounds
        #####
    
    if sCount < 8:
#             print("Start if loop")
#             print(sCount) 
#             m = ""
#         msg = ""
        for i in range(num_sounds):
#                 print(str(i) + " | " + str(sCount) + " | " + str(seq[i][sCount]))
#                 m += str(seq[i][sCount]) 
            if seq[i][sCount]:
                
                if i == 0:
                    snareTask = asyncio.create_task(playSnare(seq[i][sCount]))
#                         print("Triggering Snare")
                if i==1:
                    hhTask = asyncio.create_task(playHat(seq[i][sCount]))
                    
                if i==2:
    #                 kick.play()
                    kickTask = asyncio.create_task(playKick(seq[i][sCount]))                
#             print("End if loop")
#         await asyncio.gather()
                
                    

        

main_group.append(updateUI())
async def main():
# while True:
    global sCount
    sCount = 0
    
    while True:
        await handle_kbInput()    
        await seq_Step()
        asyncio.gather()
        
        sCount += 1

        
        #####
        # Handle Input
        #####
        


        await asyncio.sleep(delVal)
        if sCount > 7:# sCount <8:
            sCount =0


# Run Main Loop
asyncio.run(main())














