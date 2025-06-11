from PIL import Image, ImageDraw
import os

def create_blinking_eyes():
    # Create a list to store frames
    frames = []
    size = (300, 200)  # Wider size for better eye spacing
    
    # Create 15 frames for smoother animation
    for i in range(15):
        # Create a new image with transparent background
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Calculate eye openness based on frame
        if i < 5:  # Open eyes
            openness = 1.0
        elif i < 10:  # Closing
            openness = 1.0 - (i - 5) * 0.2
        elif i < 12:  # Closed
            openness = 0.0
        else:  # Opening
            openness = (i - 12) * 0.33
        
        # Draw face outline
        face_color = (255, 223, 196)  # Skin tone
        face_outline = (0, 0, 0)  # Black outline
        draw.ellipse([50, 30, 250, 170], fill=face_color, outline=face_outline, width=3)
        
        # Draw eyebrows (they move slightly when blinking)
        eyebrow_y = 60 - (5 if openness < 0.5 else 0)
        draw.arc([80, eyebrow_y, 140, eyebrow_y + 20], 0, 180, fill='black', width=3)  # Left eyebrow
        draw.arc([160, eyebrow_y, 220, eyebrow_y + 20], 0, 180, fill='black', width=3)  # Right eyebrow
        
        # Draw left eye
        left_eye_x = 90
        left_eye_y = 80
        eye_width = 50
        eye_height = int(50 * openness)
        
        # Draw eye outline
        draw.ellipse([left_eye_x-2, left_eye_y-2, left_eye_x + eye_width+2, left_eye_y + eye_height+2], 
                    fill='white', outline=face_outline, width=2)
        
        # Draw iris (only if eye is open enough)
        if openness > 0.3:
            iris_color = (0, 128, 255)  # Blue iris
            iris_size = int(eye_height * 0.6)
            iris_x = left_eye_x + (eye_width - iris_size) // 2
            iris_y = left_eye_y + (eye_height - iris_size) // 2
            draw.ellipse([iris_x, iris_y, iris_x + iris_size, iris_y + iris_size], 
                        fill=iris_color, outline=face_outline, width=1)
            
            # Draw pupil
            pupil_size = int(iris_size * 0.4)
            pupil_x = iris_x + (iris_size - pupil_size) // 2
            pupil_y = iris_y + (iris_size - pupil_size) // 2
            draw.ellipse([pupil_x, pupil_y, pupil_x + pupil_size, pupil_y + pupil_size], 
                        fill='black')
            
            # Draw highlight
            highlight_size = int(pupil_size * 0.3)
            highlight_x = pupil_x + pupil_size * 0.3
            highlight_y = pupil_y + pupil_size * 0.3
            draw.ellipse([highlight_x, highlight_y, highlight_x + highlight_size, highlight_y + highlight_size], 
                        fill='white')
        
        # Draw right eye (mirror of left eye)
        right_eye_x = 160
        right_eye_y = 80
        
        # Draw eye outline
        draw.ellipse([right_eye_x-2, right_eye_y-2, right_eye_x + eye_width+2, right_eye_y + eye_height+2], 
                    fill='white', outline=face_outline, width=2)
        
        # Draw iris (only if eye is open enough)
        if openness > 0.3:
            iris_x = right_eye_x + (eye_width - iris_size) // 2
            iris_y = right_eye_y + (eye_height - iris_size) // 2
            draw.ellipse([iris_x, iris_y, iris_x + iris_size, iris_y + iris_size], 
                        fill=iris_color, outline=face_outline, width=1)
            
            # Draw pupil
            pupil_x = iris_x + (iris_size - pupil_size) // 2
            pupil_y = iris_y + (iris_size - pupil_size) // 2
            draw.ellipse([pupil_x, pupil_y, pupil_x + pupil_size, pupil_y + pupil_size], 
                        fill='black')
            
            # Draw highlight
            highlight_x = pupil_x + pupil_size * 0.3
            highlight_y = pupil_y + pupil_size * 0.3
            draw.ellipse([highlight_x, highlight_y, highlight_x + highlight_size, highlight_y + highlight_size], 
                        fill='white')
        
        # Draw eyelashes (only when eyes are open)
        if openness > 0.8:
            # Left eye lashes
            for j in range(5):
                lash_x = left_eye_x + j * 10
                draw.line([lash_x, left_eye_y, lash_x, left_eye_y - 8], fill='black', width=2)
            # Right eye lashes
            for j in range(5):
                lash_x = right_eye_x + j * 10
                draw.line([lash_x, right_eye_y, lash_x, right_eye_y - 8], fill='black', width=2)
        
        frames.append(img)
    
    # Save as GIF
    frames[0].save('assets/blink_eyes.gif',
                  save_all=True,
                  append_images=frames[1:],
                  duration=100,  # 100ms per frame
                  loop=0)  # Loop forever

def create_water_bottle():
    # Create a list to store frames
    frames = []
    size = (200, 300)  # Increased size for better visibility
    
    # Create 12 frames for smoother animation
    for i in range(12):
        # Create a new image with transparent background
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Calculate bottle tilt based on frame
        tilt = 15 * (i - 6)  # Tilt from -90 to 90 degrees
        
        # Draw bottle body
        bottle_width = 80
        bottle_height = 200
        bottle_x = (size[0] - bottle_width) // 2
        bottle_y = 40
        
        # Draw bottle cap
        cap_width = 40
        cap_height = 30
        cap_x = (size[0] - cap_width) // 2
        cap_y = 10
        draw.rectangle([cap_x, cap_y, cap_x + cap_width, cap_y + cap_height], 
                      fill='#FFD700', outline='black', width=2)  # Gold cap
        
        # Draw bottle neck
        neck_width = 30
        neck_height = 20
        neck_x = (size[0] - neck_width) // 2
        neck_y = cap_y + cap_height
        draw.rectangle([neck_x, neck_y, neck_x + neck_width, neck_y + neck_height], 
                      fill='#E6E6FA', outline='black', width=2)  # Light purple
        
        # Draw bottle body
        bottle_color = '#E6E6FA'  # Light purple
        draw.rectangle([bottle_x, bottle_y, bottle_x + bottle_width, bottle_y + bottle_height], 
                      fill=bottle_color, outline='black', width=2)
        
        # Draw water level (moving up and down)
        water_height = 120 + int(40 * (i / 6))  # Water level varies
        water_y = bottle_y + bottle_height - water_height
        water_color = '#87CEEB'  # Sky blue
        draw.rectangle([bottle_x, water_y, bottle_x + bottle_width, bottle_y + bottle_height], 
                      fill=water_color, outline='black', width=1)
        
        # Draw water surface (wavy effect)
        wave_height = 5
        for x in range(bottle_x, bottle_x + bottle_width, 5):
            wave_y = water_y + wave_height * (i % 3)
            draw.line([x, wave_y, x + 5, wave_y + wave_height], fill='white', width=2)
        
        # Draw bubbles
        bubble_size = 8
        for j in range(3):
            bubble_x = bottle_x + 20 + j * 20
            bubble_y = water_y + 20 + (i * 10) % 40
            draw.ellipse([bubble_x, bubble_y, bubble_x + bubble_size, bubble_y + bubble_size], 
                        fill='white', outline='black', width=1)
        
        frames.append(img)
    
    # Save as GIF
    frames[0].save('assets/water_bottle.gif',
                  save_all=True,
                  append_images=frames[1:],
                  duration=100,  # 100ms per frame
                  loop=0)  # Loop forever

def main():
    # Create assets directory if it doesn't exist
    if not os.path.exists('assets'):
        os.makedirs('assets')
    
    # Generate both animations
    create_blinking_eyes()
    create_water_bottle()
    print("Animations generated successfully!")

if __name__ == "__main__":
    main()