from flask import Flask, request, abort
from flask_cors import CORS
from pathlib import Path
from datetime import datetime

from threading import Thread

base_dir = Path(__file__).parent

app = Flask("FolderMerge", template_folder=base_dir / "templates", static_folder=base_dir / "static")
CORS(app)

server_start_time = datetime.now()


@app.route("/")
def index():
    delta = datetime.now() - server_start_time
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    fmt_str = f"{delta.days} days, {hours:02}h:{minutes:02}m:{seconds:02}s"

    return f"Server up and runnning since {fmt_str}"


@app.route("/handshake", methods=["GET"])
def handshake():
    print("Hand is shaken")
    return "REQUEST set_current_session OK"


@app.route("/set_current_session", methods=["GET", "POST"])
@app.route("/set_current_session/<alias>", methods=["GET", "POST"])
def set_current_session(alias=None):
    if alias is not None:
        print(f"alias is : {alias}")
        return "REQUEST set_current_session OK"

    uuid = request.args.get("uuid", None)
    print(f"uuid is : {uuid}")
    if uuid is None:
        return abort(400, "UUID is missing")

    thread = Thread(target=manage_session_folder, args=(uuid,), kwargs={"set_as_default": True})
    thread.start()

    return "REQUEST set_current_session OK"


def manage_session_folder(uuid, set_as_default=False):
    # Perform some background work with the UUID
    print(f"Background task running with UUID: {uuid}")
    print(f"{'S' if set_as_default else 'Not '}etting the folder as default")
    from one import ONE

    cnx = ONE(data_access_mode="local")

    session = cnx.search(id=uuid, details=True)
    print(session)


class SetupConfig:
    path = Path.home() / "Downloads" / ""
    filename = "config.toml"


def run():
    app.run(host="127.0.0.1", port=52163, debug=False)


if __name__ == "__main__":
    run()
