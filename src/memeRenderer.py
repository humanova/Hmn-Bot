# 2019 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

#ffmpeg -ss 00:00:00.0 -i crab-rave.mp4 -to 00:00:29.5 -vf "drawtext=fontfile=./Raleway-Medium.ttf:text='Wollay is':fontcolor=white:fontsize=96:box=0:x=(w-text_w)/2:y=(h-text_h)/4,drawtext=fontfile=./Raleway-Medium.ttf:text='BACK':fontcolor=white:fontsize=96:box=0:x=(w-text_w)/2:y=(h-text_h)/4*3" wollay_alive.mp4

import os
import subprocess
import time
from ffmpy import FFmpeg

mRender = {
    "crabrave" : "mrender/templates/crabrave.mp4"
}

font = {
    "crabrave" : "mrender/fonts/Raleway-Medium.ttf"
}

def FixArgs(template, text):

    if template == "crabrave":
        sep = text.index('-')
        upper_text = text[0:sep]
        lower_text = text[sep + 1:]
        #out_name = str('mrender/outs/crabrave_out_'+ upper_text + lower_text + '.mp4')
        #out_name = out_name.replace(" ", "_")
        out_name = 'mrender/outs/crabrave_out_' + str(int(time.time())) + '.mp4'
        upper_text = f"'{upper_text}'"
        lower_text = f"'{lower_text}'"
        
        return [upper_text, lower_text, font['crabrave'], out_name]

def RenderMeme(template, font_size, text):

    if mRender[template]:
        r_temp = mRender[template] 
        err_msg = None

        if template == "crabrave":
            
            crab_args = FixArgs(template, text)
            out_name = crab_args[3]
            
            '''
            # if the file already exits, return its name directly
            out_files = os.listdir('mrender/outs/')
            for name in out_files:
                if name == out_name:
                    return out_name'''

            ff =  FFmpeg(
                inputs = {r_temp : '-ss 00:00:00.0 -to 00:00:29.5'},
                outputs = {out_name: f'-vf "drawtext=fontfile={crab_args[2]}:text={crab_args[0]}:fontcolor=white:fontsize={font_size}:box=0:x=(w-text_w)/2:y=(h-text_h)/4,drawtext=fontfile={crab_args[2]}:text={crab_args[1]}:fontcolor=white:fontsize={font_size}:box=0:x=(w-text_w)/2:y=(h-text_h)/4*3"'}
            )                          

            #print(f"commands :{ff.cmd}")
            print(f"preparing video : {out_name}")
        
            try :
                ff.run()

            except Exception as e: 
                
                for line in p1.stderr.readlines():
                    err_msg += line.decode('utf-8')
                    print(line)
                err_msg = '```\n' + err_msg + '```'
                print(f"py exception : {e}")

            return out_name, err_msg

    

def ClearOutVideos():

    try :
        p1 = subprocess.Popen(['rm', '--', 'mrender/outs/*'])
        p1.wait()
        return True

    except Exception as e: 
        print(e)
        return False
    