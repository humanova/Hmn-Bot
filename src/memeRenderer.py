# 2018 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

#ffmpeg -ss 00:00:00.0 -i crab-rave.mp4 -to 00:00:29.5 -vf "drawtext=fontfile=./Raleway-Medium.ttf:text='Wollay is':fontcolor=white:fontsize=96:box=0:x=(w-text_w)/2:y=(h-text_h)/4,drawtext=fontfile=./Raleway-Medium.ttf:text='BACK':fontcolor=white:fontsize=96:box=0:x=(w-text_w)/2:y=(h-text_h)/4*3" wollay_alive.mp4

import subprocess
from ffmpy import FFmpeg
#os.chmod(mRender['crabrave'], 0o775)

mRender = {
    "crabrave" : "../mrender/templates/crabrave.mp4"
}

font = "../mrender/fonts/Raleway-Medium.ttf"

def RenderMeme(template, text):

    out_name = ""
    try:
        if mRender[template]:
            r_temp = mRender[template] 

            if template == "test":
                try :
                    p1 = subprocess.Popen('ffmpeg -version')
                    p1.wait()
                    
                except Exception as e: print(e)
                return 'test'

            if template == "crabrave":
                sep = text.index('-')
                upper_text = " ".join(text[0:sep])
                lower_text = " ".join(text[sep + 1:])
                
                out_name = '../mrender/outs/crabrave_out_' + text[0] + '.mp4'

                try :
                    ff =  FFmpeg(
                        inputs = {r_temp : '-ss 00:00:00.0 -to 00:00:29.5'},
                        outputs = {out_name: '-vf "drawtext=fontfile=' + font + ':text=' + upper_text +':fontcolor=white:fontsize=96:box=0:x=(w-text_w)/2:y=(h-text_h)/4,drawtext=fontfile=' + font + ':text=' + lower_text + ':fontcolor=white:fontsize=96:box=0:x=(w-text_w)/2:y=(h-text_h)/4*3"'}
                    )
                
                    p1 = subprocess.Popen(ff.cmd)
                    p1.wait()

                except Exception as e: print(e)

                return out_name

    except:
        return
    