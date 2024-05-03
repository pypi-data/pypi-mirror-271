from abstract_pandas.excel_module import get_df,safe_excel_save
from pyxlsb import open_workbook
import pandas as pd
from pyxlsb import open_workbook as open_xlsb

import pandas as pd
df3 = pd.read_excel("/home/gamook/Downloads/ALL Time Data for Solar.xlsb", engine = 'pyxlsb')
input(df3)

