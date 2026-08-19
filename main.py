import asyncio
import edge_tts
from PIL import Image, ImageDraw, ImageFont
import subprocess

W, H = 1080, 1920

def make_img(top, main, file):
    img = Image.new('RGB', (W, H), (10, 12, 40))
    draw = ImageDraw.Draw(img)
    for y in range(H):
        draw.line([(0,y),(W,y)], fill=(10, 12, 40 + y//18))
    try:
        f1 = ImageFont.truetype("DejaVuSans-Bold.ttf", 68)
        f2 = ImageFont.truetype("DejaVuSans.ttf", 48)
    except:
        f1 = ImageFont.load_default()
        f2 = f1
    draw.text((W//2, 600), top, font=f1, fill="white", anchor="mm")
    draw.text((W//2, 900), main, font=f2, fill="#EAE6FF", anchor="mm", align="center")
    img.save(file, quality=95)

async def make_real_voices():
    # DISCIPLE - Young man, sad, broken, crying
    sad_ssml = """
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
        <voice name="en-US-GuyNeural">
            <mstts:express-as style="sad" styledegree="2">
                <prosody rate="-10%" pitch="-5%">
                    Lord... why am I suffering?
                </prosody>
            </mstts:express-as>
        </voice>
    </speak>
    """
    # JESUS - Deep, warm, calm, powerful, fatherly
    jesus_ssml = """
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
        <voice name="en-US-ChristopherNeural">
            <mstts:express-as style="calm" styledegree="2">
                <prosody rate="-15%" pitch="-20%">
                    I am preparing you... for something greater, my child.
                </prosody>
            </mstts:express-as>
        </voice>
    </speak>
    """
    print("Creating realistic sad disciple voice...")
    await edge_tts.Communicate(sad_ssml, "en-US-GuyNeural").save("v1.mp3")
    print("Creating deep Jesus voice...")
    await edge_tts.Communicate(jesus_ssml, "en-US-ChristopherNeural").save("v2.mp3")
    print("Both voices done - super realistic!")

asyncio.run(make_real_voices())

make_img("The Disciple Asked:", '"Lord, why am I suffering?"', "s1.jpg")
make_img("Jesus Replied:", '"I am preparing you\nfor something greater"', "s2.jpg")

for img, aud, out in [("s1.jpg","v1.mp3","c1.mp4"), ("s2.jpg","v2.mp3","c2.mp4")]:
    subprocess.run(["ffmpeg","-y","-loop","1","-i",img,"-i",aud,"-c:v","libx264","-c:a","aac","-shortest","-vf","scale=1080:1920,format=yuv420p","-r","30",out], check=True)

open("list.txt","w").write("file 'c1.mp4'\nfile 'c2.mp4'\n")
subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i","list.txt","-c","copy","final_video.mp4"], check=True)
print("FINAL REALISTIC VIDEO DONE!")
