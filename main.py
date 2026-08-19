from PIL import Image, ImageDraw, ImageFont
import subprocess

W, H = 1080, 1920

def make_hd(text1, text2, filename):
    img = Image.new('RGB', (W, H), (8, 10, 30))
    draw = ImageDraw.Draw(img)
    # Simple HD gradient background
    for y in range(H):
        r = int(8 + y*0.05)
        b = int(30 + y*0.1)
        draw.line([(0,y),(W,y)], fill=(r,10,b))
    
    # Add text - centered
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
        font_small = ImageFont.truetype("DejaVuSans.ttf", 42)
    except:
        font = ImageFont.load_default()
        font_small = font

    draw.text((W//2, 700), text1, font=font, fill=(255,255,255), anchor="mm", stroke_width=2, stroke_fill=(0,0,0))
    draw.text((W//2, 1000), text2, font=font_small, fill=(230,230,255), anchor="mm", align="center")
    img.save(filename, quality=95)
    print(f"Created {filename} at 1080x1920")

make_hd("The Disciple Asked:", '"Lord, why am I suffering?"', "scene1.jpg")
make_hd("Jesus Replied:", '"I am preparing you\nfor something greater"', "scene2.jpg")

# Create video from images using ffmpeg - FULL HD, no CapCut
cmd = [
    "ffmpeg", "-y",
    "-loop", "1", "-t", "3.5", "-i", "scene1.jpg",
    "-loop", "1", "-t", "3.5", "-i", "scene2.jpg",
    "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0,format=yuv420p,scale=1080:1920:flags=lanczos",
    "-r", "30",
    "-b:v", "6000k",
    "final_video.mp4"
]
subprocess.run(cmd, check=True)
print("HD VIDEO DONE!")
