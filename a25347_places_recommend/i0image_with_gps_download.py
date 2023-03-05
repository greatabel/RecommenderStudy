import requests
from bs4 import BeautifulSoup
from PIL import Image

# URL of the Weibo page containing the images
url = "https://weibo.com/3738542481/MfRG2AOzK#comment"

# Make a GET request to the URL
response = requests.get(url)

# Parse the HTML content of the response with BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find all the image tags in the HTML
image_tags = soup.find_all("img")

print('image_tags##########', image_tags)

# Loop through the image tags
for img in image_tags:
    # Get the URL of the image
    img_url = img.get("src")
    
    # Make a GET request to the image URL
    img_response = requests.get(img_url)
    
    # Download the image to a file
    with open("image.jpg", "wb") as f:
        f.write(img_response.content)
    
    # Load the image with Pillow
    pil_image = Image.open("image.jpg")
    
    # Get the GPS information from the image metadata
    gps_info = pil_image._getexif().get(34853)
    
    # Print the GPS information (if available)
    if gps_info:
        print(f"GPS Info: {gps_info}")
    
    # Delete the image file
    os.remove("image.jpg")
