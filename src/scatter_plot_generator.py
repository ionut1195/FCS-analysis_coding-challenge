import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Tuple, Union
import logging


class ScatterPlotGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def normalize_data(self, data: np.ndarray) -> np.ndarray:
        """Normalize data to 0-1 range with handling for edge cases"""
        min_val = np.percentile(data, 1)
        max_val = np.percentile(data, 99)
        normalized = np.clip((data - min_val) / (max_val - min_val), 0, 1)
        return normalized

    def generate_density_scatterplot(
        self,
        x_data: np.ndarray,
        y_data: np.ndarray,
        image_size: Tuple[int, int] = (256, 256),
        save_path: Union[str, Path] = "scatterplot.png",
        title: str = None,
    ) -> Path:
        """
        Generate an enhanced density-based scatterplot with exact dimensions.
        """
        save_path = Path(save_path)
        print(save_path)

        # Set figure size in inches and DPI to achieve exact pixel dimensions
        dpi = 100
        width_inches = image_size[0] / dpi
        height_inches = image_size[1] / dpi

        # Create figure with fixed size
        plt.clf()  # Clear any existing plots
        fig = plt.figure(figsize=(width_inches, height_inches), dpi=dpi)

        # Set axes to occupy the entire figure
        ax = plt.axes([0, 0, 1, 1])

        # Normalize data
        x_norm = self.normalize_data(x_data)
        y_norm = self.normalize_data(y_data)

        # Create density scatter plot
        plt.hist2d(
            x_norm,
            y_norm,
            bins=50,  # Reduced bins for better visualization
            cmap="viridis",
            norm=plt.matplotlib.colors.LogNorm(),
        )

        # Optional title with smaller font to fit
        if title:
            plt.title(title, pad=2, fontsize=8)

        # Remove axes and make plot compact
        plt.axis("off")

        # Save with exact dimensions
        plt.savefig(save_path, dpi=dpi, bbox_inches="tight", pad_inches=0, format="png")

        # Ensure exact size using PIL
        from PIL import Image

        img = Image.open(save_path)
        img = img.resize(image_size, Image.Resampling.LANCZOS)
        img.save(save_path)

        plt.close(fig)

        self.logger.info(f"Scatter plot saved to {save_path}")
        return save_path

    def generate_scatter_matrix(
        self,
        data: dict,
        save_dir: Union[str, Path],
        image_size: Tuple[int, int] = (256, 256),
    ) -> list:
        """
        Generate scatter plots for all channel combinations
        """
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)

        generated_plots = []
        channels = list(data.keys())

        for i, channel1 in enumerate(channels):
            for channel2 in channels[i + 1 :]:
                plot_name = f"scatter_{channel1}_vs_{channel2}.png"
                save_path = save_dir / plot_name.replace(" ", "_")

                self.generate_density_scatterplot(
                    data[channel1],
                    data[channel2],
                    image_size=image_size,
                    save_path=save_path,
                    title=f"{channel1} vs {channel2}",
                )
                generated_plots.append(save_path)

        return generated_plots

    def verify_output(self, image_path: Union[str, Path]) -> bool:
        """Verify the generated image meets requirements"""
        try:
            from PIL import Image

            img = Image.open(image_path)

            # Check dimensions
            if img.size != (256, 256):
                self.logger.error(f"Invalid image dimensions: {img.size}")
                return False

            # Check if image is not empty
            img_array = np.array(img)
            if np.mean(img_array) < 1:  # Check if image is not too dark
                self.logger.error("Generated image appears to be empty")
                return False

            return True

        except Exception as e:
            self.logger.error(f"Error verifying image: {str(e)}")
            return False
