from PIL import Image, ImageDraw
import os

def generate_settings_icon():
    size = (128, 128)
    img = Image.new('RGBA', size, (255, 255, 255, 255))  # White background
    draw = ImageDraw.Draw(img)

    # Draw face (bigger and centered)
    face_center = (64, 56)
    face_radius = 28
    draw.ellipse([
        face_center[0] - face_radius, face_center[1] - face_radius,
        face_center[0] + face_radius, face_center[1] + face_radius
    ], fill=(255, 224, 189), outline=(120, 80, 60), width=4)

    # Draw hair (simple arc, thicker)
    draw.arc([
        face_center[0] - face_radius - 6, face_center[1] - face_radius - 12,
        face_center[0] + face_radius + 6, face_center[1] + face_radius + 18
    ], start=200, end=340, fill=(80, 50, 30), width=12)

    # Draw body (torso, larger)
    draw.rectangle([52, 82, 76, 112], fill=(120, 180, 255), outline=(80, 120, 180), width=4)

    # Draw arms (yoga pose, cross-legged, thicker)
    # Left arm
    draw.line([52, 88, 32, 112], fill=(255, 224, 189), width=10)
    # Right arm
    draw.line([76, 88, 96, 112], fill=(255, 224, 189), width=10)

    # Draw legs (crossed, bolder)
    # Left leg
    draw.line([56, 112, 36, 124], fill=(120, 180, 255), width=12)
    # Right leg
    draw.line([72, 112, 92, 124], fill=(120, 180, 255), width=12)

    # Draw simple eyes (dots, bigger)
    draw.ellipse([58, 54, 62, 58], fill=(60, 60, 60))
    draw.ellipse([66, 54, 70, 58], fill=(60, 60, 60))

    # Draw a small smile (bolder)
    draw.arc([60, 62, 68, 70], start=20, end=160, fill=(120, 80, 60), width=2)

    # Save icon
    if not os.path.exists('assets'):
        os.makedirs('assets')
    img.save('assets/settings_icon.png')
    print('Icon saved as assets/settings_icon.png')

if __name__ == "__main__":
    generate_settings_icon()