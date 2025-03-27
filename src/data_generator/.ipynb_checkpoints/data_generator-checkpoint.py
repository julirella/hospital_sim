from src.importer import GenImporter


class DataGenerator:
    def __init__(self, people_file: str, layout_file: str):
        self.gen_importer = GenImporter(people_file, layout_file)
        self.gen_importer.import_data()

# def med_shift_plan(people_file: str, layout_file: str, out_file: str, shift_length: int, meds_per_shift: int):
    # ...
#   for each nurse, figure out amount of patients

    def max_graph_dst(self):
        return self.gen_importer.max_graph_dst()