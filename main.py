from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
import subprocess

W, H = 1080, 1920

def make_img(top, main, file):
    img = Image.new('RGB', (W, H), (12, 12, 35))
    draw = ImageDraw.Draw(img)
    for y in range(H):
        draw.line([(0,y),(W,y)], fill=(12, 12, 35 + y//20))
    try:
        f1 = ImageFont.truetype("DejaVuSans-Bold.ttf", 68)
        f2 = ImageFont.truetype("DejaVuSans.ttf", 46)
    except:
        f1 = ImageFont.load_default()
        f2 = f1
    draw.text((W//2, 650), top, font=f1, fill="white", anchor="mm")
    draw.text((W//2, 950), main, font=f2, fill="#E6E6FF", anchor="mm", align="center")
    img.save(file, quality=95)
    print(f"Made {file}")

# TRY VOICE - if fails, still make video
try:
    print("Generating AI voice...")
    gTTS(text="Lord, why am I suffering?", lang='en').save("v1.mp3")
    gTTS(text="I am preparing you for something greater, my child.", lang='en').save("v2.mp3")
    HAS_VOICE = True
    print("Voice OK")
except Exception as e:
    print(f"Voice failed {e} - making silent HD video")
    HAS_VOICE = False

make_img("The Disciple Asked:", '"Lord, why am I suffering?"', "s1.jpg")
make_img("Jesus Replied:", '"I am preparing you\nfor something greater"', "s2.jpg")

if HAS_VOICE:
    for img, aud, out in [("s1.jpg","v1.mp3","c1.mp4"), ("s2.jpg","v2.mp3","c2.mp4")]:
        subprocess.run(["ffmpeg","-y","-loop","1","-i",img,"-i",aud,"-c:v","libx264","-c:a","aac","-shortest","-vf","scale=1080:1920,format=yuv420p","-r","30",out], check=True)
    open("list.txt","w").write("file 'c1.mp4'\nfile 'c2.mp4'\n")
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i","list.txt","-c","copy","final_video.mp4"], check=True)
else:
    subprocess.run(["ffmpeg","-y","-loop","1","-t","3","-i","s1.jpg","-loop","1","-t","3","-i","s2.jpg","-filter_complex","[0:v][1:v]concat=n=2:v=1:a=0,scale=1080:1920,format=yuv420p[v]","-map","[v]","-r","30","final_video.mp4"], check=True)

print("DONE!")
