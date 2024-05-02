import pandas as pd

from pathlib import Path

from xurpas_data_quality.render.renderer import HTMLBase
from xurpas_data_quality.data.dataframe import load_dataframe, validate_dataframe
from xurpas_data_quality.data.describe import describe
from xurpas_data_quality.report import get_report

"""def get_data_quality_report():
    return HTMLBase(body=None, name='Manhour Utilization Summary').render()

def to_file(file_path:str, file_name:str="report.html"):
    output = Path(file_path+ "/" + file_name)
    print(f"saving to {file_path}")
    output.write_text(get_data_quality_report(), encoding='utf-8')
    print(f"saved!")"""


class DataReport:
    def __init__(self, df:str):
        if df is None:
            raise ValueError("there must be an input!")
        self.df = load_dataframe(df)
        
    def describe_dataframe(self):
        self.description = describe(self.df)

    def get_data_quality_report(self, name=None):
        self.describe_dataframe()
        report = get_report(self.description, name=name)
        return report.render()
    
    def to_file(self, file_path:str, file_name:str="report.html"):
        output = Path(file_path+ "/" + file_name)
        print(f"saving to {file_path}")
        output.write_text(self.get_data_quality_report(), encoding='utf-8')
        print(f"saved!")