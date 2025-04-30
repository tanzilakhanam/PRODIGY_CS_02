from PIL import Image
import random

def encrypt_image(image_path):
    img = Image.open(image_path)
    img = img.convert("RGBA")  # Ensure 4 channels
    pixels = list(img.getdata())
    width, height = img.size

    # Invert colors
    inverted_pixels = []
    for p in pixels:
        r, g, b, a = p
        inverted_pixels.append((255 - r, 255 - g, 255 - b, a))

    # Shuffle pixels
    random.shuffle(inverted_pixels)

    # Create new encrypted image
    encrypted_img = Image.new("RGBA", (width, height))
    encrypted_img.putdata(inverted_pixels)
    encrypted_img.save("encrypted_image.png")
    print("🔐 Encrypted image saved as 'encrypted_image.png'")

    # Save the shuffled index map for decryption
    with open("key_map.txt", "w") as f:
        for i, pixel in enumerate(pixels):
            f.write(f"{i}\n")
    print("🗝️ Key map saved as 'key_map.txt'")

def decrypt_image(image_path, width, height):
    encrypted_img = Image.open(image_path)
    encrypted_img = encrypted_img.convert("RGBA")
    encrypted_pixels = list(encrypted_img.getdata())

    # Read original order
    with open("key_map.txt", "r") as f:
        indices = list(map(int, f.readlines()))

    # Reorder pixels back to original positions
    decrypted_pixels = [None] * len(encrypted_pixels)
    for new_index, original_index in enumerate(indices):
        r, g, b, a = encrypted_pixels[new_index]
        decrypted_pixels[original_index] = (255 - r, 255 - g, 255 - b, a)  # Re-invert

    # Create decrypted image
    decrypted_img = Image.new("RGBA", (width, height))
    decrypted_img.putdata(decrypted_pixels)
    decrypted_img.save("decrypted_image.png")
    print("🔓 Decrypted image saved as 'decrypted_image.png'")

def main():
    print("=== Image Encryption Tool ===")
    choice = input("Do you want to (E)ncrypt or (D)ecrypt? ").strip().upper()

    if choice == 'E':
        image_path = input("Enter the path to the image: ").strip()
        encrypt_image(image_path)
    elif choice == 'D':
        image_path = input("Enter the path to the encrypted image: ").strip()
        width = int(input("Enter the original width of the image: "))
        height = int(input("Enter the original height of the image: "))
        decrypt_image(image_path, width, height)
    else:
        print("Invalid choice. Use 'E' or 'D'.")

if __name__ == "__main__":
    main()
