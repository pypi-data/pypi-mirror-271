import pandas as pd
import pathlib as pl


def rename_folders(df: pd.DataFrame, subs_folder: pl.Path) -> None:
    """
    Renames folders in subs_folder based on a DataFrame mapping of names to student IDs.

    Args:
        df (pd.DataFrame): DataFrame containing columns 'Last Name', 'First Name', and 'Student ID'.
        subs_folder (Path): pathlib.Path object pointing to the directory containing the folders to be renamed.
    """
    # Convert DataFrame to a dictionary for easier lookup
    name_id_map = {
        (row["Last Name"].upper(), row["First Name"].upper()): row["Student ID"]
        for _, row in df.iterrows()
    }

    def ask_to_rename(folder_name, suggested_name):
        """Prompts user for rename confirmation."""
        response = (
            input(f"Rename '{folder_name}' to '{suggested_name}'? (y/n): ")
            .strip()
            .lower()
        )
        return response == "y"

    rename_attempts = []  # Initialize a list to keep track of rename attempts

    for folder in subs_folder.iterdir():
        if not folder.is_dir():
            continue

        folder_name_upper = folder.name.upper()
        matched = False

        for (last_name, first_name), student_id in name_id_map.items():
            if last_name in folder_name_upper and first_name in folder_name_upper:
                new_folder_name = f"{last_name}, {first_name} ({student_id})"
                try:
                    folder.rename(subs_folder / new_folder_name)
                    print(f"Folder renamed for {new_folder_name}")
                    outcome = "Renamed"
                except Exception as e:
                    print(f"Failed to rename folder for {new_folder_name}: {e}")
                    outcome = "Failed"
                rename_attempts.append(
                    {
                        "Original Name": folder.name,
                        "Suggested Name": new_folder_name,
                        "Outcome": outcome,
                    }
                )
                matched = True
                break

        if not matched:
            for (last_name, first_name), student_id in name_id_map.items():
                if f" {first_name} " in folder_name_upper:
                    new_folder_name = f"{last_name}, {first_name} ({student_id})"
                elif f" {last_name} " in folder_name_upper:
                    new_folder_name = f"{last_name}, {first_name} ({student_id})"
                else:
                    continue

                if ask_to_rename(folder.name, new_folder_name):
                    try:
                        folder.rename(subs_folder / new_folder_name)
                        outcome = "User Confirmed"
                    except Exception as e:
                        print(f"Failed to rename folder for {new_folder_name}: {e}")
                        outcome = "Failed After User Confirmation"
                else:
                    outcome = "User Rejected"
                rename_attempts.append(
                    {
                        "Original Name": folder.name,
                        "Suggested Name": new_folder_name,
                        "Outcome": outcome,
                    }
                )
                matched = True
                break

        if not matched:
            rename_attempts.append(
                {
                    "Original Name": folder.name,
                    "Suggested Name": "N/A",
                    "Outcome": "No Match Found",
                }
            )
