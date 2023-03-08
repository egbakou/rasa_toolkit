TRAINED_MODEL_PATH = "models/"
DOMAIN_DIRECTORY_PATH = "./"
TEMP_DIR = "rasa_toolkit/"

def update_rasa_model(trained_model_path: str = TRAINED_MODEL_PATH,
                      domain_directory_path: str = DOMAIN_DIRECTORY_PATH):
    """
    Updates the latest Rasa model with the domain files in the domain_directory_path.
    :param trained_model_path: Path to the directory containing the latest Rasa model. By default, this is models/
    :param domain_directory_path: Path to the directory containing the domain files. Default is ./
    :return:
    """
    # Step 1: Clean up temp directory
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR)

    # Step 2: Load domain files
    domain = Domain.from_directory(domain_directory_path)

    # Step 3: Merge domain files
    domain.persist(f"{TEMP_DIR}domain.yml")

    # Step 4: Get the latest model and its name
    model_archive_path = get_latest_model(trained_model_path)
    print(f"model_path: {model_archive_path}")
    # get model name from the path without extension
    model_name = Path(model_archive_path).stem
    # remove .tar from model name
    model_name = model_name[:-4]

    # Step 5: Unpack the model archive
    storage_path = Path(f"{TEMP_DIR}{model_name}")
    # if storage_path exists, delete it
    if storage_path.exists():
        shutil.rmtree(storage_path)
    # extract all files from the model archive to storage_path
    with TarSafe.open(model_archive_path, "r:gz") as tar:
        tar.extractall(storage_path)

    # Step 6: Remove the old domain file from the unpacked model archive
    old_domain_file_path = Path(f"{storage_path}/components/domain_provider/domain.yml")
    old_domain_file_path.unlink()

    # Step 7: Copy new domain file to the unpacked model archive
    if not os.path.exists(f"{storage_path}/components/domain_provider"):
        os.makedirs(f"{storage_path}/components/domain_provider")
    shutil.copyfile(f"{TEMP_DIR}domain.yml", f"{storage_path}/components/domain_provider/domain.yml")

    # Step 8: Update metadata.json in the unpacked model archive
    json_metadata = read_json_file(f"{storage_path}/metadata.json")
    json_metadata["domain"] = domain.as_dict()
    dump_obj_as_json_to_file(f"{storage_path}/metadata.json", json_metadata)

    # Step 9: archive the storage_path directory using TarSafe
    archive_path = Path(f"{TEMP_DIR}{model_name}.tar.gz")
    with TarSafe.open(archive_path, "w:gz") as tar:
        tar.add(storage_path, arcname="")

    # remove storage_path directory
    shutil.rmtree(storage_path)

if __name__ == "__main__":
    # Update the latest Rasa model after updating responses in the domain files
    update_rasa_model(domain_directory_path="data/domain/")
