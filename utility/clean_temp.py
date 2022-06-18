import shutil

def clean_cache():
    shutil.rmtree("./Applications./__pycache__",ignore_errors=True)
    shutil.rmtree("./utility/__pycache__",ignore_errors=True)
    shutil.rmtree("./__pycache__/",ignore_errors=True)