import pytest
import numpy as np
from pathlib import Path
from PIL import Image
import tempfile
import os
import sys
from src.scatter_plot_generator import ScatterPlotGenerator

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)


@pytest.fixture
def scatter_generator():
    """Fixture to create a ScatterPlotGenerator instance"""
    return ScatterPlotGenerator()


@pytest.fixture
def sample_data():
    """Fixture to create sample data for testing"""
    np.random.seed(42)  # For reproducible tests
    return {
        "channel1": np.random.normal(0, 1, 1000),
        "channel2": np.random.normal(0, 1, 1000),
        "channel3": np.random.normal(0, 1, 1000),
    }


@pytest.fixture
def temp_output_dir():
    """Fixture to create and cleanup a temporary directory"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


def test_normalize_data(scatter_generator, sample_data):
    """Test data normalization"""
    normalized = scatter_generator.normalize_data(sample_data["channel1"])
    assert np.all((normalized >= 0) & (normalized <= 1))
    assert len(normalized) == len(sample_data["channel1"])


def test_scatter_matrix_generation(scatter_generator, sample_data, temp_output_dir):
    """Test scatter matrix generation"""
    generated_plots = scatter_generator.generate_scatter_matrix(
        sample_data, save_dir=temp_output_dir
    )

    # Check number of plots (for n channels, should have n*(n-1)/2 plots)
    n_channels = len(sample_data)
    expected_plots = (n_channels * (n_channels - 1)) // 2
    assert len(generated_plots) == expected_plots

    # Check each generated plot
    for plot_path in generated_plots:
        assert Path(plot_path).exists()
        with Image.open(plot_path) as img:
            assert img.size == (256, 256)
            # Check if image is not empty (has some content)
            img_array = np.array(img)
            assert np.mean(img_array) > 1


def test_invalid_data_handling(scatter_generator, temp_output_dir):
    """Test handling of invalid input data"""
    output_path = temp_output_dir / "invalid_test.png"

    # Test with empty arrays
    with pytest.raises(Exception):
        scatter_generator.generate_density_scatterplot(
            np.array([]), np.array([]), save_path=output_path
        )

    # Test with arrays of different lengths
    with pytest.raises(Exception):
        scatter_generator.generate_density_scatterplot(
            np.array([1, 2, 3]), np.array([1, 2]), save_path=output_path
        )


def test_title_rendering(scatter_generator, sample_data, temp_output_dir):
    """Test scatter plot with title"""
    output_path = temp_output_dir / "title_test.png"
    test_title = "Test Plot"

    scatter_generator.generate_density_scatterplot(
        sample_data["channel1"],
        sample_data["channel2"],
        save_path=output_path,
        title=test_title,
    )

    assert output_path.exists()
    with Image.open(output_path) as img:
        assert img.size == (256, 256)
