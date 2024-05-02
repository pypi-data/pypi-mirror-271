import argparse
from flask import Flask, request, jsonify, send_from_directory
from tinydb import TinyDB, Query
import os
import base64
import uuid
import shutil
import copy

app = Flask(__name__)

# db = TinyDB("data.json")
# db = None


def save_blob(base64_data):
    """Save blob data and return the blob filepath."""
    binary_data = base64.b64decode(base64_data.encode())
    filename = f"{str(uuid.uuid4())}_{hash(binary_data)}.blob"
    filepath = os.path.join(BLOB_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(binary_data)
    return filename


def handle_blob_for_dict(data_dict, original_dict=None):
    """Handle blob data in a dictionary."""
    for key, value in data_dict.items():
        if isinstance(value, dict) and value.get("type") == "blob":
            filepath = save_blob(value["data"])
            data_dict[key] = {"type": "blob", "filepath": filepath}

            # If an original dictionary is provided and it had a blob for this key, delete the old blob
            if original_dict:
                original_blob_info = original_dict.get(key)
                if (
                    isinstance(original_blob_info, dict)
                    and original_blob_info.get("type") == "blob"
                ):
                    os.remove(original_blob_info["filepath"])


def convert_blob_file_to_base64(filepath):
    """Convert blob file to a base64 encoded string."""
    filepath = os.path.join(BLOB_DIR, filepath)
    with open(filepath, "rb") as f:
        binary_data = f.read()
    return base64.b64encode(binary_data).decode()


def handle_blobs_in_fetched_data(data, fetch_blob):
    """Replace blob references with a dictionary containing type and base64 encoded content in fetched data."""
    if fetch_blob:
        for item in data:
            for key, value in item.items():
                if isinstance(value, dict) and value.get("type") == "blob":
                    base64_content = convert_blob_file_to_base64(value["filepath"])
                    item[key] = {"type": "blob", "data": base64_content}


@app.route("/log_data", methods=["POST"])
def log_data():
    data = request.json
    data["entry_id"] = str(uuid.uuid4())  # Assign a unique ID
    handle_blob_for_dict(data)
    db.insert(data)
    return jsonify(
        {"message": "Data logged successfully!", "entry_id": data["entry_id"]}
    )


@app.route("/get_data", methods=["POST"])
def get_data():
    criteria_data = request.json
    criteria = criteria_data["criteria"]
    fetch_blob = criteria_data.get("fetch_blob", False)

    Data = Query()
    query = None

    # Construct the query based on criteria
    for key, value in criteria.items():
        # Check if the value contains a wildcard
        if "*" in value:
            value = value.replace("*", ".*")  # Convert * to .* for regex matching
            current_condition = Data[key].matches(value)
        else:
            current_condition = Data[key] == value

        if query:
            query &= current_condition
        else:
            query = current_condition

    results = db.search(query)
    results = copy.deepcopy(
        results
    )  # Avoid modifying the original data on the database (in memory part of the db. the orginal file is not modified)
    handle_blobs_in_fetched_data(results, fetch_blob)
    return jsonify(results)


@app.route("/modify_data/<entry_id>", methods=["PUT"])
def modify_data(entry_id):
    modifications = request.json
    Data = Query()
    entry = db.search(Data["entry_id"] == entry_id)

    if not entry:
        return jsonify({"error": "Entry not found!"}), 404

    handle_blob_for_dict(modifications, entry[0])
    db.update(modifications, Data["entry_id"] == entry_id)
    return jsonify({"message": "Data modified successfully!"})


@app.route("/reset_database", methods=["POST"])
def reset_database():
    db.truncate()

    if os.path.exists(BLOB_DIR):
        shutil.rmtree(BLOB_DIR)
    os.makedirs(BLOB_DIR)

    return jsonify({"message": "Database and blobs reset successfully!"})


@app.route("/delete_data", methods=["POST"])
def delete_data():
    criteria = request.json
    Data = Query()
    query = None

    for key, value in criteria.items():
        if "*" in str(value):
            value = str(value).replace("*", ".*")  # Convert * to .* for regex matching
            current_condition = Data[key].matches(value)
        else:
            current_condition = Data[key] == value

        if query:
            query &= current_condition
        else:
            query = current_condition

    matching_entries = db.search(query)

    # If blobs were associated, delete them
    for entry in matching_entries:
        for key, value in entry.items():
            if isinstance(value, dict) and value.get("type") == "blob":
                try:
                    os.remove(value["filepath"])
                except FileNotFoundError:
                    pass

    deleted_count = db.remove(query)

    return jsonify({"message": f"Deleted {deleted_count} entries."})


def main():
    global db, BLOB_DIR
    parser = argparse.ArgumentParser(description="Start the FinallyDataLogger server.")
    parser.add_argument(
        "--dir", type=str, default="./data", help="Directory for data storage."
    )
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="Host address to run the server on.",
    )
    parser.add_argument(
        "--port", type=int, default=5000, help="Port number to run the server on."
    )

    args = parser.parse_args()

    BLOB_DIR = os.path.join(os.getcwd(), args.dir, "blobs")
    print("BLOB_DIR: ", BLOB_DIR)
    db_path = os.path.join(args.dir, "data.json")
    if not os.path.exists(BLOB_DIR):
        os.makedirs(BLOB_DIR)
    db = TinyDB(db_path)

    app.run(host=args.host, port=args.port)
    # app.run(port=args.port)


if __name__ == "__main__":
    main()
