from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import os

W, H = 1080, 1920

def make_hd(t1, t2, filename):
    img = Image.new('RGB', (W, H), (8, 10, 30))
    draw = ImageDraw.Draw(img)
    for y in range(H):
        r = int(8 + y*0.05)
        b = int(30 + y*0.1)
        draw.line([(0,y),(W,y)], fill=(r,10,b))
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 70)
        font_small = ImageFont.truetype("DejaVuSans.ttf", 48)
    except:
        font = ImageFont.load_default()
        font_small = font
    draw.text((W//2, 700), t1, font=font, fill=(255,255,255), anchor="mm", stroke_width=2, stroke_fill=(0,0,0))
    draw.text((W//2, 1050), t2, font=font_small, fill=(230,230,255), anchor="mm", align="center")
    img.save(filename, quality=95, dpi=(300,300))
    print(f"Made {filename}")

# 1. MAKE VOICE FIRST
print("Making voice...")
gTTS(text="Lord, why am I suffering?", lang='en', slow=False).save("voice1.mp3")
gTTS(text="I am preparing you for something greater, my child.", lang='en', slow=False).save("voice2.mp3")

# 2. MAKE IMAGES
make_hd("The Disciple Asked:", '"Lord, why am I suffering?"', "scene1.jpg")
make_hd("Jesus Replied:", '"I am preparing you\nfor something greater"', "scene2.jpg")

# 3. MAKE VIDEO WITH VOICE SYNCED
print("Making video with voice...")
audio1 = AudioFileClip("voice1.mp3")
audio2 = AudioFileClip("voice2.mp3")

clip1 = ImageClip("scene1.jpg").set_duration(audio1.duration + 0.8).set_audio(audio1)
clip2 = ImageClip("scene2.jpg").set_duration(audio2.duration + 0.8).set_audio(audio2)

final = concatenate_videoclips([clip1, clip2], method="compose")
final.write_videofile("final_video.mp4", fps=24, codec='libx264', audio_codec='aac', bitrate="5000k")
print("DONE - VIDEO WITH VOICE READY!")
