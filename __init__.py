from CTFd.utils.user import get_current_user
import requests
from flask import Blueprint, jsonify
from CTFd.models import db, Challenges
from CTFd.plugins.challenges import CTFdStandardChallenge, CHALLENGE_CLASSES
from CTFd.plugins.challenges import (
    CTFdStandardChallenge,
    CHALLENGE_CLASSES,
)
from CTFd.plugins import register_plugin_assets_directory
payload = {}
headers = {
'X-API-KEY': 'AD.zxSCk8jbiQIKUFSCr5fD9sPb5P2iWXmo2qp7bh9m'    ##need to put something here and also swap and remove it from when I have finished
}

class LudusChallenge(Challenges):
    __mapper_args__ = {"polymorphic_identity": "ludus"}

    id = db.Column(
        None,
        db.ForeignKey("challenges.id"),
        primary_key=True
    )

class LudusChallenger(BaseChallenge):
    id = "ludus"
    name = "Ludus"
    challenge_model = LudusChallenge    


class Ranges(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ludus_user_id = db.Column(db.String(128), nullable=False, unique=True)
    ctfd_user = db.Column(db.String(128), nullable=True)

    def __init__(self, team, location):
        self.target = team
        self.location = location

ludus_bp = Blueprint(
    "ludus_ranges",
    __name__,
    url_prefix="/ludus_ranges",
    static_folder="assets"
)

@ludus_bp.route("/challenges/<int:challenge_id>")
def challenge_info(challenge_id):
##list ranges accessible to the user
##list range vms, power state and  testing /range
    url = "https://172.28.252.105:8080/api/v2/range"
    user = get_current_user().name
    #user = "TP"
        ##insert ludus server ip api thingy here
    params = {
    "rangeID": assign_user(user),
    "userID": user,
    "details": False #do you want to return OS version, license, update info, etc
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=10,
        verify=False
    )

    print(response.text)
    return jsonify({"kali_ip": kali_ip})



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
    db_setup()
    db.create_all()
    
    register_plugin_assets_directory(
        app,
        base_path="/plugins/challenges/assets/"
    )
    CHALLENGE_CLASSES["ludus"] = LudusChallenge
 
##creating the database to assign ctfd users to
def db_setup():
    url = "https://172.28.252.105:8080/api/v2/user/all"
    all_ludus_users = (requests.request("GET", url, headers=headers, data=payload, verify=False)).json()
    print(all_ludus_users)
    user_ids = [
        user["userID"]
        for user in all_ludus_users
    ]
    for user_id in user_ids:
        new_user = Ranges(user_id, None)
        db.session.add(new_user)
    db.session.commit
