from CTFd.utils.user import get_current_user
import requests
from flask import Blueprint, jsonify, Response
from CTFd.models import db, Challenges
from CTFd.plugins.challenges import BaseChallenge, CHALLENGE_CLASSES
from CTFd.plugins import register_plugin_assets_directory
IP_ADDRESS = "192.168.2.100"
payload = {}
headers = {
'X-API-KEY': 'AD.zxSCk8jbiQIKUFSCr5fD9sPb5P2iWXmo2qp7bh9m'    ##need to put something here and also swap and remove it from when I have finished
}

class LudusChallengeModel(Challenges):
    __mapper_args__ = {"polymorphic_identity": "ludus"}
    id = db.Column(None, db.ForeignKey("challenges.id"), primary_key=True)

class LudusChallenge(BaseChallenge):
    id = "ludus"
    name = "Ludus"
    challenge_model = LudusChallengeModel
    templates = {
        "create": "/plugins/ludus-project/assets/create.html",
        "update": "/plugins/ludus-project/assets/update.html",
        "view": "/plugins/ludus-project/assets/view.html",
    }

    scripts = {
        "create": "/plugins/ludus-project/assets/create.js",
        "update": "/plugins/ludus-project/assets/update.js",
        "view": "/plugins/ludus-project/assets/view.js",
    }

class Ranges(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ludus_user_id = db.Column(db.String(128), nullable=False, unique=True)
    ctfd_user = db.Column(db.String(128), nullable=True)

    def __init__(self, ludus_user_id, ctfd_user=None):
        self.ludus_user_id = ludus_user_id
        self.ctfd_user = ctfd_user

ludus_bp = Blueprint(
    "ludus_ranges",
    __name__,
    url_prefix="/ludus_ranges",
    static_folder="assets"
)

# @ludus_bp.route("/challenges/<int:challenge_id>")
@ludus_bp.route("/challenges")
def challenge_info():   ##don't need parameter here?
##list ranges accessible to the user
##list range vms, power state and  testing /range
    user = get_current_user().name
    ludus_user = assign_user(user)
    url = f"https://{IP_ADDRESS}:8080/api/v2/ranges/accessible"     ##fetch range for user 
    params = {"userID": ludus_user}
    user_range = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=10,
        verify=False
    )
    print("URL:", user_range.url)
    print("Status:", user_range.status_code)
    print("Body:", user_range.text)

    user_range = user_range.json()
    rangeID = user_range[0]["rangeID"]

    url = f"https://{IP_ADDRESS}:8080/api/v2/range"        ##fetch range ip for user
    params = {
    "rangeID": rangeID,   
    "userID": ludus_user,
    "details": False #do you want to return OS version, license, update info, etc
    }

    range_details = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=10,
        verify=False
    ).json()

    print(range_details)
    device_name = ludus_user + "-kali"
    print("device name: " + device_name)
    for vm in range_details.get("VMs", []):
        if vm.get("name") == device_name:
            kali_ip = vm.get("ip")
            print(kali_ip)

    return jsonify({"range_id": kali_ip, "kali_ip": kali_ip})

@ludus_bp.route("/wireguard/config")
def wireguard_conf():
    user = get_current_user().name
    ludus_user = assign_user(user)  ##can i reduce this to a global var
    url = f"https://{IP_ADDRESS}:8080/api/v2/user/wireguard"
    params = {"userID": ludus_user}
    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=10,
        verify=False
    ).json()

    config = response["result"]["wireGuardConfig"]
    return Response(
    config,
    mimetype="text/plain",
    headers={
        "Content-Disposition": 'attachment; filename="ludus.conf"'
    }
)

@ludus_bp.route("/test")
def test():
    user = get_current_user()
    print(user.id)
        

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email
    })

def assign_user(user):
    range_user = Ranges.query.filter_by(ctfd_user=user).first()
    if not range_user:
        available = Ranges.query.filter_by(ctfd_user=None).first()
        available.ctfd_user = user
        db.session.commit()
        return available.ludus_user_id
    else:
        return range_user.ludus_user_id


def load(app):
    app.register_blueprint(ludus_bp)
    Ranges.__table__.drop(db.engine, checkfirst=True)
    db.create_all()
    db_setup()
    
    register_plugin_assets_directory(
        app,
        base_path="/plugins/ludus-project/assets/"
    )
    CHALLENGE_CLASSES["ludus"] = LudusChallenge
    print("AVAILABLE CHALLENGE TYPES:", CHALLENGE_CLASSES.keys())
 
##creating the database to assign ctfd users to
def db_setup():
    url = f"https://{IP_ADDRESS}:8080/api/v2/user/all"
    all_ludus_users = (requests.request("GET", url, headers=headers, data=payload, verify=False)).json()
    print(all_ludus_users)
    user_ids = [
        user["userID"]
        for user in all_ludus_users
    ]
    for user_id in user_ids:
        new_user = Ranges(user_id, None)
        db.session.add(new_user)
    db.session.commit()
