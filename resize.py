import os
from PIL import Image
import fitz  # PyMuPDF
import io

def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def resize_image(image_path, output_path, max_size=(1024, 1024)):
    with Image.open(image_path) as img:
        img.thumbnail(max_size)
        img.save(output_path)
        print(f"Resized image saved to {output_path}")

def resize_pdf_images(pdf_path, output_dir, max_size=(1024, 1024)):
    pdf_document = fitz.open(pdf_path)
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image = Image.open(io.BytesIO(image_bytes))
            image.thumbnail(max_size)
            output_image_path = os.path.join(output_dir, f"{os.path.basename(pdf_path)}_page_{page_num + 1}_image_{img_index + 1}.{image_ext}")
            image.save(output_image_path)
            print(f"Resized image from PDF saved to {output_image_path}")

def process_directory(input_dir, output_dir, max_size=(1024, 1024)):
    ensure_directory(output_dir)

    for root, _, files in os.walk(input_dir):
        for file in files:
            file_path = os.path.join(root, file)
            output_path = os.path.join(output_dir, file)
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
                resize_image(file_path, output_path, max_size)
            elif file.lower().endswith('.pdf'):
                pdf_output_dir = os.path.join(output_dir, os.path.splitext(file)[0])
                ensure_directory(pdf_output_dir)
                resize_pdf_images(file_path, pdf_output_dir, max_size)

if __name__ == "__main__":
    input_directory = "figures"
    output_directory = "resizedfigures"
    max_size = (1024, 1024)  # Set the maximum size for resizing

    process_directory(input_directory, output_directory, max_size)
