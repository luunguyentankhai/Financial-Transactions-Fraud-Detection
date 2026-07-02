from os.path import exists
from pathlib import Path

Base_Dir = Path(__file__).resolve().parent.parent.parent

Data_Dir = Base_Dir / "data"

# check folder data have exist 
Data_Dir.mkdir(parents=True, exist_ok=True)

Process_Dir = Data_Dir / "processed"

Raw_Dir = Data_Dir / "raw"

# check folder Process and Raw have exist
Process_Dir.mkdir(parents=True, exist_ok=True)
Raw_Dir.mkdir(parents=True, exist_ok=True)


Root_Data_File = Raw_Dir / "Data.csv"

sql_dir = Base_Dir / "src" / "db" / "sql_queries"

logs_dir = Base_Dir / "logs"
logs_dir.mkdir(parents=True,exist_ok=True)

Assets_Dir = Process_Dir / "Assets"
Assets_Dir.mkdir(parents=True, exist_ok=True)

Models_Dir = Process_Dir / "Models"
Models_Dir.mkdir(parents=True, exist_ok=True)
