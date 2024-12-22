from scatter_plot_generator import ScatterPlotGenerator
from data_loader import FCSLoader
from pathlib import Path
from model_handler import ModelHandler
import json


def main():
    loader = FCSLoader()
    meta, data = loader.load_file("src/0001[WDF].fcs")
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

    model_handler = ModelHandler()
    results = {}

    for plot_path in generated_plots:
        if generator.verify_output(plot_path):
            plot_name = plot_path.stem
            prediction = model_handler.predict(plot_path)
            results[plot_name] = prediction

    # Save predictions
    with open(output_dir / "predictions.json", "w") as f:
        json.dump(results, f, indent=4)


if __name__ == "__main__":
    main()
