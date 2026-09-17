import pathlib


script_dir_path = pathlib.Path(__file__).parent.resolve()

first_names = open(f'{script_dir_path}/replacement_data/first_names.txt').read().splitlines()
last_names = open(f'{script_dir_path}/replacement_data/last_names.txt').read().splitlines()
thesis_titles_fi = open(f'{script_dir_path}/replacement_data/thesis_titles_fi.txt').read().splitlines()
thesis_titles_en = open(f'{script_dir_path}/replacement_data/thesis_titles_en.txt').read().splitlines()
thesis_titles_sv = open(f'{script_dir_path}/replacement_data/thesis_titles_sv.txt').read().splitlines()
person_titles_en = open(f'{script_dir_path}/replacement_data/person_titles_en.txt').read().splitlines()
person_titles_sv = open(f'{script_dir_path}/replacement_data/person_titles_sv.txt').read().splitlines()
