import logging
import os
import threading
from PIL import Image, ImageTk, ImageDraw
from PIL.Image import Image as PILImage
from PIL.ImageDraw import ImageDraw as PILImageDraw

class ImageProcessor:
    def __init__(self) -> None:
        self.preview_image: PILImage | None = None
        self.original_image: PILImage | None = None
        self.processed_image: PILImage | None = None

        self.processing_thread: threading.Thread | None = None
        self.stop_processing: bool = False

        self._logger: logging.Logger = logging.getLogger(__name__)

    def load_image(self, image_path) -> PILImage:
        try:
            self.original_image = Image.open(image_path).convert("RGBA")
            return self.original_image
        except Exception as e:
            raise Exception(f"Failed to load image: {str(e)}")

    def process_image(self, image: PILImage, options):
        """Process an image with the given options"""
        try:
            # Make a copy to avoid modifying the original
            img: PILImage = image.copy()

            # Resize if needed
            if options["resize"] and options["width"] > 0 and options["height"] > 0:
                img = img.resize((options["width"], options["height"]), Image.LANCZOS)

            # Crop if needed
            if options["crop"]:
                img = img.crop((options["crop_left"], options["crop_top"],
                    options["crop_right"], options["crop_bottom"]))

            # Add border
            img_draw: PILImageDraw = ImageDraw.Draw(img)  
            img_draw.rectangle((0, 0, img.width - 1, img.height - 1), outline ="red")

            # Process transparency and colors
            if options["background_mode"] == "custom":
                # Custom color transparency
                bg_color = options["custom_color"]
                tolerance = options["tolerance"] / 100.0

                new_data = []
                for item in img.getdata():
                    r, g, b, a = item

                    # Calculate color distance (simple Euclidean distance)
                    distance = (
                        ((r - bg_color[0]) / 255) ** 2 +
                        ((g - bg_color[1]) / 255) ** 2 +
                        ((b - bg_color[2]) / 255) ** 2
                    ) ** 0.5

                    if distance < tolerance:
                        # Background → transparent
                        new_data.append((0, 0, 0, 0))
                    elif options["invert_colors"]:
                        # Invert non-background colors if requested
                        new_data.append((255 - r, 255 - g, 255 - b, a))
                    else:
                        # Keep original colors
                        new_data.append((r, g, b, a))
            else:
                # Black or white background
                new_data = []

                if options["background_mode"] == "black":
                    # Black background
                    tolerance = options["tolerance"]
                    for item in img.getdata():
                        r, g, b, a = item
                        # Check if pixel is close to black
                        if r <= tolerance and g <= tolerance and b <= tolerance:
                            # Black background → transparent
                            new_data.append((0, 0, 0, 0))
                        elif options["invert_colors"]:
                            if r > 240 and g > 240 and b > 240:
                                # White → black
                                new_data.append((0, 0, 0, 255))
                            else:
                                # Other colors → invert
                                new_data.append((255 - r, 255 - g, 255 - b, a))
                        else:
                            # Keep original colors
                            new_data.append((r, g, b, a))
                else:
                    # White background
                    tolerance = 255 - options["tolerance"]
                    for item in img.getdata():
                        r, g, b, a = item
                        # Check if pixel is close to white
                        if r >= tolerance and g >= tolerance and b >= tolerance:
                            # White background → transparent
                            new_data.append((0, 0, 0, 0))
                        elif options["invert_colors"]:
                            if r < 15 and g < 15 and b < 15:
                                # Black → white
                                new_data.append((255, 255, 255, 255))
                            else:
                                # Other colors → invert
                                new_data.append((255 - r, 255 - g, 255 - b, a))
                        else:
                            # Keep original colors
                            new_data.append((r, g, b, a))

            img.putdata(new_data)

            # Apply alpha adjustment if needed
            if options["adjust_alpha"] and options["alpha_value"] < 255:
                alpha_value = options["alpha_value"]
                alpha_data = []
                for item in img.getdata():
                    r, g, b, a = item
                    if a > 0:  # Only adjust non-transparent pixels
                        new_alpha = min(a, alpha_value)
                        alpha_data.append((r, g, b, new_alpha))
                    else:
                        alpha_data.append((r, g, b, a))
                img.putdata(alpha_data)

            # Apply background replacement if needed
            if options["replace_background"]:
                bg_img = Image.new("RGBA", img.size, options["replacement_color"])
                img = Image.alpha_composite(bg_img, img)

            return img

        except Exception as e:
            raise Exception(f"Error processing image: {str(e)}")

    def get_image_preview(self, image: PILImage, max_size=(300, 300)):
        """Create a thumbnail preview of the image"""
        if image is None:
            return None

        # Create a copy to avoid modifying the original
        img: PILImage = image.copy()
        img.thumbnail(max_size)
        return ImageTk.PhotoImage(img)

    def save_image(self, image: PILImage, output_path, format_option, quality=95, optimize=True, preserve_metadata=False):
        """Save the processed image"""
        try:
            # Get the appropriate format and extension
            format_map = {
                "png": "PNG",
                "jpg": "JPEG",
                "jpeg": "JPEG",
                "webp": "WEBP",
                "tiff": "TIFF",
                "bmp": "BMP"
            }

            format_name = format_map.get(format_option.lower(), "PNG")

            # Ensure the output path has the correct extension
            base, _ = os.path.splitext(output_path)
            output_path = f"{base}.{format_option.lower()}"

            # Handle JPEG format (no alpha channel)
            if format_name == "JPEG":
                # Create a white background
                bg = Image.new("RGB", image.size, (255, 255, 255))
                bg.paste(image, (0, 0), image)

                # Save with quality setting
                bg.save(output_path, format=format_name, quality=quality, optimize=optimize)
            else:
                # Save with appropriate settings for the format
                if format_name == "PNG":
                    image.save(output_path, format=format_name, optimize=optimize)
                elif format_name == "WEBP":
                    image.save(output_path, format=format_name, quality=quality, lossless=quality > 90)
                elif format_name == "BMP":
                    image.convert(mode='P', colors=16).save(output_path, format=format_name)
                else:
                    image.save(output_path, format=format_name)

            return output_path
        except Exception as e:
            raise Exception(f"Failed to save image: {str(e)}")

