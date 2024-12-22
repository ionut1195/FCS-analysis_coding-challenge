from scatter_plot_generator import ScatterPlotGenerator
from data_loader import FCSLoader
from pathlib import Path


def main():
    loader = FCSLoader()
    meta, data = loader.load_file("./src/0001[WDF].fcs")
    channels = loader.get_channels(meta)

    # Create dictionary of all channel data
    channel_data = {channel: data[channel] for channel in channels}

    # Initialize generator
    generator = ScatterPlotGenerator()

    output_dir = Path("scatter_plots")
    output_dir.mkdir(exist_ok=True)

    generated_plots = generator.generate_scatter_matrix(
        channel_data, save_dir=output_dir
    )
    for i in generated_plots:
        generator.verify_output(i)


if __name__ == "__main__":
    main()
