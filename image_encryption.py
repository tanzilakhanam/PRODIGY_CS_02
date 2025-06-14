from PIL import Image
import random

# Function to encrypt an image
def encrypt_image(image_path):
    # Open the image and ensure it has 4 channels (RGBA)
    img = Image.open(image_path)
    img = img.convert("RGBA")
    pixels = list(img.getdata())  # Get image pixel data as a list
    width, height = img.size

    # Step 1: Invert each pixel's RGB values (keep alpha same)
    inverted_pixels = []
    for p in pixels:
        r, g, b, a = p
        inverted_pixels.append((255 - r, 255 - g, 255 - b, a))

    # Step 2: Shuffle the pixels randomly
    random.shuffle(inverted_pixels)

    # Step 3: Create new encrypted image from shuffled pixels
    encrypted_img = Image.new("RGBA", (width, height))
    encrypted_img.putdata(inverted_pixels)
    encrypted_img.save("encrypted_image.png")
    print("🔐 Encrypted image saved as 'encrypted_image.png'")

    # Save the index map (original order) for use during decryption
    with open("key_map.txt", "w") as f:
        for i, pixel in enumerate(pixels):
            f.write(f"{i}\n")
    print("🗝️ Key map saved as 'key_map.txt'")

# Function to decrypt an image
def decrypt_image(image_path, width, height):
    # Load the encrypted image
    encrypted_img = Image.open(image_path)
    encrypted_img = encrypted_img.convert("RGBA")
    encrypted_pixels = list(encrypted_img.getdata())

    # Read the saved index order from key_map.txt
    with open("key_map.txt", "r") as f:
        indices = list(map(int, f.readlines()))

    # Step 1: Unshuffle the pixels based on the original index map
    decrypted_pixels = [None] * len(encrypted_pixels)
    for new_index, original_index in enumerate(indices):
        r, g, b, a = encrypted_pixels[new_index]
        # Step 2: Re-invert the color values to get the original
        decrypted_pixels[original_index] = (255 - r, 255 - g, 255 - b, a)

    # Step 3: Create new decrypted image
    decrypted_img = Image.new("RGBA", (width, height))
    decrypted_img.putdata(decrypted_pixels)
    decrypted_img.save("decrypted_image.png")
    print("🔓 Decrypted image saved as 'decrypted_image.png'")

# Entry point of the script
def main():
    print("=== Image Encryption Tool ===")
    choice = input("Do you want to (E)ncrypt or (D)ecrypt? ").strip().upper()

    if choice == 'E':
        # Encrypt an image
        image_path = input("Enter the path to the image: ").strip()
        encrypt_image(image_path)

    elif choice == 'D':
        # Decrypt an image
        image_path = input("Enter the path to the encrypted image: ").strip()
        width = int(input("Enter the original width of the image: "))
        height = int(input("Enter the original height of the image: "))
        decrypt_image(image_path, width, height)

    else:
        print("Invalid choice. Use 'E' for Encrypt or 'D' for Decrypt.")

# Only run main if this file is executed directly
if __name__ == "__main__":
    main()
