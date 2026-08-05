import csv
import json
import zipfile
import os
import argparse
import sys

from utils import parse_custom_fields


def main():
    # Configure argument parser
    parser = argparse.ArgumentParser(
        description="Convert a Bitwarden export ZIP to JSON."
    )
    parser.add_argument(
        "zip_filepath",
        help="Path to the export ZIP file"
    )
    parser.add_argument(
        "output_dir",
        nargs="?",
        default=".",
        help="Output directory (default: current directory)"
    )
    args = parser.parse_args()

    zip_filepath = args.zip_filepath
    output_dir = args.output_dir

    # Validate input file exists
    if not os.path.isfile(zip_filepath):
        print(f"Error: '{zip_filepath}' does not exist or is not a file.", file=sys.stderr)
        sys.exit(1)

    # Extract the ZIP archive
    with zipfile.ZipFile(zip_filepath, "r") as zf:
        zf.extractall()

    dump = {"folders": [], "items": []}

    # Process Folders.csv
    with open("Folders.csv", "r", encoding="utf-8") as f:
        folder_structure = {}
        folders = []

        reader = csv.DictReader(f)
        for row in reader:
            if row["ParentLabel"] == "Home":
                folder_structure[row["Id"]] = row["Label"]
                dump["folders"].append({"id": row["Id"], "name": row["Label"]})
            elif row["ParentId"] in folder_structure:
                path = row["ParentLabel"] + "/" + row["Label"]
                folder_structure[row["Id"]] = path
                dump["folders"].append({"id": row["Id"], "name": path})
            else:
                folders.append({
                    "parent_id": row["ParentId"],
                    "id": row["Id"],
                    "name": row["Label"]
                })

        # Reconstruct folder hierarchy safely
        while folders:
            remaining = []
            for folder in folders:
                if folder["parent_id"] in folder_structure:
                    path = folder_structure[folder["parent_id"]] + "/" + folder["name"]
                    folder_structure[folder["id"]] = path
                    dump["folders"].append({"id": folder["id"], "name": path})
                else:
                    remaining.append(folder)
            folders = remaining

    # Process Passwords.csv
    with open("Passwords.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dump["items"].append({
                "id": row["Id"],
                "organizationId": None,
                "folderId": row["Folder Id"],
                "type": 1,
                "name": row["Label"],
                "notes": row["Notes"],
                "favorite": True if "Favorite" in row and row["Favorite"] == "true" else False,
                "login": {
                    "username": row["Username"],
                    "password": row["Password"],
                    "totp": None,
                    "uris": [{"match": None, "uri": row["Url"]}],
                },
                "fields": parse_custom_fields(row["Custom Fields"]),
                "collectionIds": [],
            })

    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Save to the output directory
    output_file = os.path.join(output_dir, "dump.json")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(json.dumps(dump, indent=4))

    print(f"Done! Upload {output_file} to Bitwarden or Vaultwarden.")


if __name__ == "__main__":
    main()
