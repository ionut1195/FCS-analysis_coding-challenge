from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pathlib import Path
import shutil
import tempfile
from .data_loader import FCSLoader
from .scatter_plot_generator import ScatterPlotGenerator
from .model_handler import ModelHandler
import json

app = FastAPI(title="RobotDreams FCS Analysis API")


@app.post("/upload-fcs/")
async def upload_fcs(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_path = Path(temp_file.name)

    loader = FCSLoader()
    meta, data = loader.load_file(temp_path)
    channels = loader.get_channels(meta)
    channel_data = {channel: data[channel] for channel in channels}

    generator = ScatterPlotGenerator()
    output_dir = Path("scatter_plots")
    output_dir.mkdir(exist_ok=True)

    plots = generator.generate_scatter_matrix(channel_data, save_dir=output_dir)

    model_handler = ModelHandler()
    results = {}

    for plot_path in plots:
        if generator.verify_output(plot_path):
            plot_name = plot_path.stem
            prediction = model_handler.predict(plot_path)
            results[plot_name] = prediction

    with open(output_dir / "predictions.json", "w") as f:
        json.dump(results, f, indent=4)
    temp_path.unlink()

    return {"plots": [str(p) for p in plots], "predictions": results}


@app.get("/plot/{plot_name}")
async def get_plot(plot_name: str):
    plot_path = Path("scatter_plots") / f"{plot_name}"
    if not plot_path.exists():
        raise HTTPException(status_code=404, detail="Plot Not Found")
    return FileResponse(
        plot_path,
        media_type="image/png",
        headers={"Content-Disposition": f"attachment; filename={plot_name}"},
    )


@app.get("/predictions/")
async def get_predictions():
    pred_path = Path("scatter_plots") / "predictions.json"
    if not pred_path.exists():
        raise HTTPException(status_code=404, detail="Predictions Not Found")
    with open(pred_path) as f:
        return json.load(f)
