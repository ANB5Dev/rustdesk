#!/usr/bin/env python3

import os
import sys
import io
import cairosvg
from PIL import Image


def main():

    if len(sys.argv) < 2:
        print("Usage: generate_images.py <name>")
        sys.exit(1)

    input_folder = 'customization/images/'+sys.argv[1]

    print(f"Generating custom images from folder '{input_folder}'")
    
    # Output details (see process_logo())
    output_files = [
        {"filename": "res/32x32.png", "type": "icon-squarebg", "width": 32, "height": 32},
        {"filename": "res/64x64.png", "type": "icon-squarebg", "width": 64, "height": 64},
        {"filename": "res/128x128.png", "type": "icon-squarebg", "width": 128, "height": 128},
        {"filename": "res/128x128@2x.png", "type": "icon-squarebg", "width": 256, "height": 256},
        {"filename": "res/icon.ico", "type": "icon-squarebg", "width": 128, "height": 128},
        {"filename": "res/icon.png", "type": "icon-squarebg", "width": 1024, "height": 1024},
        {"filename": "res/logo.svg", "type": "icon-squarebg"},
        {"filename": "res/mac-icon.png", "type": "icon-squarebg", "width": 1024, "height": 1024},
        {"filename": "res/scalable.svg", "type": "icon-squarebg"},
        {"filename": "res/tray-icon.ico", "type": "icon-silhouette", "width": 32, "height": 32},

        # Universal
        {"filename": "flutter/assets/logo.png", "type": "logo"},  # in-app logo

        # Windows
        {"filename": "flutter/windows/runner/resources/app_icon.ico", "type": "icon-nobg", "width": 48, "height": 48},  # Windows exe icon
        {"filename": "libs/portable/src/res/label.png", "type": "logo", "width": 96, "height": 32},  # Windows self-extracting boot logo

        # macOS
        {"filename": "flutter/macos/Runner/AppIcon.icns", "type": "icon-squarebg"},  # macOS app icon
        {"filename": "flutter/assets/icon.png", "type": "icon-silhouette", "width": 26, "height": 26},  # macOS tray icon (was icon-nobg)

        # Android
        {"filename": "flutter/android/app/src/main/res/mipmap-hdpi/ic_launcher.png", "type": "icon-squarebg", "width": 72, "height": 72, "pad%": 10 },
        {"filename": "flutter/android/app/src/main/res/mipmap-hdpi/ic_launcher_foreground.png", "type": "icon-nobg", "width": 162, "height": 162, "pad%": 25 },
        {"filename": "flutter/android/app/src/main/res/mipmap-hdpi/ic_launcher_round.png", "type": "icon-roundbg", "width": 72, "height": 72, "pad%": 5 },
        {"filename": "flutter/android/app/src/main/res/mipmap-hdpi/ic_stat_logo.png", "type": "icon-silhouette", "width": 36, "height": 36}, # tray icon

        {"filename": "flutter/android/app/src/main/res/mipmap-mdpi/ic_launcher.png", "type": "icon-squarebg", "width": 48, "height": 48, "pad%": 10 },
        {"filename": "flutter/android/app/src/main/res/mipmap-mdpi/ic_launcher_foreground.png", "type": "icon-nobg", "width": 108, "height": 108, "pad%": 25 },
        {"filename": "flutter/android/app/src/main/res/mipmap-mdpi/ic_launcher_round.png", "type": "icon-roundbg", "width": 48, "height": 48, "pad%": 5 },
        {"filename": "flutter/android/app/src/main/res/mipmap-mdpi/ic_stat_logo.png", "type": "icon-silhouette", "width": 24, "height": 24},

        {"filename": "flutter/android/app/src/main/res/mipmap-xhdpi/ic_launcher.png", "type": "icon-squarebg", "width": 96, "height": 96, "pad%": 10 },
        {"filename": "flutter/android/app/src/main/res/mipmap-xhdpi/ic_launcher_foreground.png", "type": "icon-nobg", "width": 216, "height": 216, "pad%": 25 },
        {"filename": "flutter/android/app/src/main/res/mipmap-xhdpi/ic_launcher_round.png", "type": "icon-roundbg", "width": 96, "height": 96, "pad%": 5 },
        {"filename": "flutter/android/app/src/main/res/mipmap-xhdpi/ic_stat_logo.png", "type": "icon-silhouette", "width": 48, "height": 48},

        {"filename": "flutter/android/app/src/main/res/mipmap-xxhdpi/ic_launcher.png", "type": "icon-squarebg", "width": 144, "height": 144, "pad%": 10 },
        {"filename": "flutter/android/app/src/main/res/mipmap-xxhdpi/ic_launcher_foreground.png", "type": "icon-nobg", "width": 324, "height": 324, "pad%": 25 },
        {"filename": "flutter/android/app/src/main/res/mipmap-xxhdpi/ic_launcher_round.png", "type": "icon-roundbg", "width": 144, "height": 144, "pad%": 5 },
        {"filename": "flutter/android/app/src/main/res/mipmap-xxhdpi/ic_stat_logo.png", "type": "icon-silhouette", "width": 72, "height": 72},

        {"filename": "flutter/android/app/src/main/res/mipmap-xxxhdpi/ic_launcher.png", "type": "icon-squarebg", "width": 192, "height": 192, "pad%": 10 },
        {"filename": "flutter/android/app/src/main/res/mipmap-xxxhdpi/ic_launcher_foreground.png", "type": "icon-nobg", "width": 432, "height": 432, "pad%": 25 },
        {"filename": "flutter/android/app/src/main/res/mipmap-xxxhdpi/ic_launcher_round.png", "type": "icon-roundbg", "width": 192, "height": 192, "pad%": 5 },
        {"filename": "flutter/android/app/src/main/res/mipmap-xxxhdpi/ic_stat_logo.png", "type": "icon-silhouette", "width": 96, "height": 96},
    ]

    for output_file in output_files:
        process_logo(input_folder=input_folder, details=output_file)


def process_logo(input_folder, details):
    """
    Processes an SVG/PNG file to generate PNG, ICO, and SVG outputs with specific resolutions.

    :param input_filename_base: directory with the input files, excl. type and extension.
    :param output_details: List of output file details, each a dict with keys:
        - filename: The output file path.
        - type: "icon-nobg"/"icon-roundbg"/"icon-squarebg"/"icon-silhouette"/"logo".
        - width: Width of the output (not for SVG output, optional for type=logo).
        - height: Height of the output (not for SVG output, optional for type=logo).
        - pad%: Percentage of transparent padding (optional, only for SVG->PNG).
    """

    output_file = input_folder + '/generated/' + details["filename"]
    type = details.get("type", "no")
    width = details.get("width", None)
    height = details.get("height", None)
    padding = details.get("pad%", 0)
    
    ext = os.path.splitext(output_file)[1].lower()
    input_icon_svg_path = f'{input_folder}/{type}.svg'
    input_logo_path = f'{input_folder}/{type}.png'

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    if ext == ".svg":
        with open(input_icon_svg_path, 'rb') as src_file:
            with open(output_file, 'wb') as dest_file:
                dest_file.write(src_file.read())
        print(f"SVG copied to: {output_file}")

    elif ext == ".png":

        if type == "logo":
            if width is None and height is None:
                # move PNG
                with open(input_logo_path, 'rb') as png_file:
                    with open(output_file, 'wb') as dest_file:
                        dest_file.write(png_file.read())
                print(f"PNG copied to: {output_file}")

            else:
                # resize PNG
                with Image.open(input_logo_path) as png_file:
                    png_file.thumbnail((width, height))  # resize naar max. width x height, met behoud van aspect ratio
                    png_file.save(output_file)
                print(f"PNG saved to: {output_file}")

        else:
            # Convert to PNG

            # write without border
            pad_x = int(width * padding/100)
            pad_y = int(height * padding/100)
            with open(input_icon_svg_path, "rb") as svg_file:
                png_data = cairosvg.svg2png(
                    file_obj=svg_file,
                    output_width=width - 2 * pad_x,
                    output_height=height - 2 * pad_y
                )

            # place on larger canvas and save
            inner_img = Image.open(io.BytesIO(png_data)).convert("RGBA")
            final_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            final_img.paste(inner_img, (pad_x, pad_y))
            final_img.save(output_file)

            print(f"PNG saved to: {output_file}")

    elif ext == ".ico":
        # Convert to ICO (via PNG intermediate)
        temp_png_path = output_file.replace(".ico", ".png")
        with open(input_icon_svg_path, "rb") as svg_file:
            cairosvg.svg2png(
                file_obj=svg_file,
                write_to=temp_png_path,
                output_width=width,
                output_height=height,
            )
        Image.open(temp_png_path).save(output_file, format="ICO")
        os.remove(temp_png_path)
        print(f"ICO saved to: {output_file}")

    elif ext == ".icns":
        # Convert to ICNS (via PNG intermediates)
        images = []
        for size in [16, 32, 64, 128, 256, 512, 1024]:
            temp_png_path = output_file.replace(".icns", ".png")
            border_width = int(size*0.0977)
            
            # save SVG to PNG
            with open(input_icon_svg_path, "rb") as svg_file:
                cairosvg.svg2png(
                    file_obj=svg_file,
                    write_to=temp_png_path,
                    output_width=size - 2*border_width,
                    output_height=size - 2*border_width,
                )

            # add border around it
            new_image = Image.new("RGBA", (size, size), (0, 0, 0, 0))  # Transparent background
            image = Image.open(temp_png_path).convert("RGBA")
            new_image.paste(image, (border_width, border_width))  # Center the original image

            # add to list of images
            images.append( new_image )
            os.remove(temp_png_path)        

        # Save all sizes into a single ICNS file
        images[0].save(output_file, format="ICNS", append_images=images[1:])
        print(f"ICNS saved to: {output_file}")


    else:
        print(f"unknown extension: {ext}, skipping")


if __name__ == "__main__":
    main()