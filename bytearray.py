# Read the image file as bytes
with open('known_faces.png', 'rb') as file:
    image_bytes = file.read()

# Convert the image bytes to a list of integers
byte_list = list(image_bytes)

# Format the byte list as a string
byte_string = '[' + ', '.join(str(b) for b in byte_list) + ']'

# Write the byte string to a text file
with open('image.txt', 'w') as file:
    file.write(byte_string)