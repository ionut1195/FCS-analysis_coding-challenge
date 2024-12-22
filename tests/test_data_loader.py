from src.data_loader import FCSLoader


def test_fcs_loader():
    loader = FCSLoader()

    meta, data = loader.load_file("./src/0001[WDF].fcs")
    assert meta is not None
    assert data is not None

    channels = loader.get_channels(meta)
    assert len(channels) > 0
