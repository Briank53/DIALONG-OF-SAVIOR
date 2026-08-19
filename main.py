from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS

# 1. Settings
BG = "/mnt/data/desert_sunset_walk.webp" # replace with your image or use AI gen
# For GitHub you will upload your own desert.jpg

def make_scene(input_img, text, output_name):
    img = Image.open(input_img).convert("RGB")
    W,H = 1080, 1920
    canvas = Image.new("RGB", (W,H), "black")
    # resize
    base = Image.open(input_img).resize((W, int(W * 0.75)))
    canvas.paste(base, (0, 500))

    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
    except:
        font = ImageFont.load_default()

    # Caption box - TikTok style
    draw.rectangle([0, 1450, 1080, 1750], fill="black")
    draw.text((40, 1500), text, font=font, fill="white", stroke_width=4, stroke_fill="black")
    canvas.save(output_name)
    print(f"Saved {output_name}")

# 2. Make 2 scenes
make_scene("desert.jpg", "To what place are we going?", "scene1.jpg")
make_scene("desert.jpg", "Stand in a place you can reach.", "scene2.jpg")

# 3. Make voices - two men
# Disciple - younger voice (UK)
tts1 = gTTS("To what place are we going?", lang='en', tld='co.uk')
tts1.save("disciple.mp3")

# Jesus - older, slower voice (US)
tts2 = gTTS("Stand in a place you can reach.", lang='en', tld='com', slow=True)
tts2.save("jesus.mp3")

print("Done! Now you have 2 images + 2 voices. Use CapCut to combine.")
