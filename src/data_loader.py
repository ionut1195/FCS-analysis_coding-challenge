import fcsparser
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations


class FCSLoader:
    def load_file(self, file_path):
        meta, data = fcsparser.parse(file_path)
        return meta, data

    def get_channels(self, meta):
        return [meta[f"$P{i}S"] for i in range(1, meta.get("$PAR") + 1)]


# for channel in channels:
#     print(f"channel {channel}-> {data[channel]}")


# def generate_scatterplot_image(
#     x_data, y_data, image_size=(256, 256), save_path="scatterplot.png"
# ):
#     """
#     Generate a 256x256 scatterplot image from the provided data.

#     Args:
#     - x_data: Data for the x-axis (channel data).
#     - y_data: Data for the y-axis (channel data).
#     - image_size: Size of the output image (default is 256x256).
#     - save_path: Path to save the generated PNG image.
#     """
#     # Normalize the data to fit within a 256x256 grid (image size)
#     x_normalized = np.clip(
#         np.interp(x_data, (x_data.min(), x_data.max()), (0, image_size[0] - 1)),
#         0,
#         image_size[0] - 1,
#     )
#     y_normalized = np.clip(
#         np.interp(y_data, (y_data.min(), y_data.max()), (0, image_size[1] - 1)),
#         0,
#         image_size[1] - 1,
#     )

#     # Convert normalized data to integer indices
#     x_int = x_normalized.astype(int)
#     y_int = y_normalized.astype(int)

#     # Create an empty image with black background
#     image = np.zeros(image_size, dtype=np.uint8)

#     # Mark the scatter plot points as white (255)
#     for x, y in zip(x_int, y_int):
#         image[y, x] = 255  # Mark the pixel as white (255)

#     # Save the image as a PNG file
#     plt.imshow(image, cmap="gray", origin="upper")
#     plt.axis("off")  # Turn off axes
#     plt.savefig(save_path, bbox_inches="tight", pad_inches=0)
#     plt.close()  # Close the plot to avoid displaying it


# channel_pairs = combinations(channels, 2)

# for i, (x_channel, y_channel) in enumerate(channel_pairs):
#     # Extract data for the selected channels
#     x_data = data[x_channel]
#     y_data = data[y_channel]

#     # Generate a scatterplot image and save it
#     save_path = f"scatterplot_{x_channel}_{y_channel}.png"
#     generate_scatterplot_image(x_data, y_data, save_path=save_path)

#     print(f"Scatter plot saved as: {save_path}")
