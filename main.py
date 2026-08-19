from PIL import Image, ImageDraw, ImageFont
import subprocess
import asyncio
import os

async def make_voice():
    try:
        import edge_tts
        # Disciple voice - sad young man
        t1 = edge_tts.Communicate('"Lord, why am I suffering?"', "en-US-GuyNeural")
        await t1.save("voice1.mp3")
        # Jesus voice - deep calm
        t2 = edge_tts.Communicate('"I am preparing you for something greater"', "en-US-ChristopherNeural")
        await t2.save("voice2.mp3")
        print("Voices created")
        return True
    except Exception as e:
        print(f"TTS failed {e}")
        return False

W, H = 1080, 1920
def make_hd(t1, t2, filename):
    img = Image.new('RGB', (W, H), (8, 10, 30))
    draw = ImageDraw.Draw(img)
    for y in range(H):
        r = int(8 + y*0.05)
        b = int(30 + y*0.1)
        draw.line([(0,y),(W,y)], fill=(r,10,b))
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 65)
        font_small = ImageFont.truetype("DejaVuSans.ttf", 45)
    except:
        font = ImageFont.load_default()
        font_small = font
    draw.text((W//2, 700), t1, font=font, fill=(255,255,255), anchor="mm", stroke_width=2, stroke_fill=(0,0,0))
    draw.text((W//2, 1000), t2, font=font_small, fill=(230,230,255), anchor="mm", align="center")
    img.save(filename, quality=95)

asyncio.run(make_voice())
make_hd("The Disciple Asked:", '"Lord, why am I suffering?"', "scene1.jpg")
make_hd("Jesus Replied:", '"I am preparing you\nfor something greater"', "scene2.jpg")

# Build video WITH VOICE using ffmpeg
has_voice = os.path.exists("voice1.mp3")
if has_voice:
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", "3.5", "-i", "scene1.jpg",
        "-loop", "1", "-t", "3.5", "-i", "scene2.jpg",
        "-i", "voice1.mp3", "-i", "voice2.mp3",
        "-filter_complex",
        "[0:v][1:v]concat=n=2:v=1:a=0,format=yuv420p,scale=1080:1920:flags=lanczos[v];[2:a][3:a]concat=n=2:v=0:a=1[a]",
        "-map", "[v]", "-map", "[a]",
        "-r", "30", "-b:v", "6000k",
        "final_video.mp4"
    ]
else:
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", "3.5", "-i", "scene1.jpg",
        "-loop", "1", "-t", "3.5", "-i", "scene2.jpg",
        "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0,format=yuv420p,scale=1080:1920:flags=lanczos",
        "-r", "30", "-b:v", "6000k",
        "final_video.mp4"
    ]

subprocess.run(cmd, check=True)
print("FINAL VIDEO WITH VOICE DONE!")
