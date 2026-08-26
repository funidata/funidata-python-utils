import pathlib


script_dir_path = pathlib.Path(__file__).parent.resolve()

first_names = open(f'{script_dir_path}/replacement_data/first_names.txt').read().splitlines()
last_names = open(f'{script_dir_path}/replacement_data/last_names.txt').read().splitlines()
thesis_names = open(f'{script_dir_path}/replacement_data/thesis_names.txt').read().splitlines()
titles_en = open(f'{script_dir_path}/replacement_data/titles_en.txt').read().splitlines()
titles_sv = open(f'{script_dir_path}/replacement_data/titles_sv.txt').read().splitlines()
