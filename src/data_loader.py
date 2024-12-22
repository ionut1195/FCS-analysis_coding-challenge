import fcsparser


class FCSLoader:
    def load_file(self, file_path):
        meta, data = fcsparser.parse(file_path)
        return meta, data

    def get_channels(self, meta):
        return [meta[f"$P{i}S"] for i in range(1, meta.get("$PAR") + 1)]
