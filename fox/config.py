from pydantic import BaseModel


class Config(BaseModel):
    cache_base_folder_path: str = "./Cache/"
    cache_dep_uuid_file_name: str = "dep_uuid_list.json"
    target_url: str = "https://timetable.nycu.edu.tw/"

    save_dep_result: bool = True
