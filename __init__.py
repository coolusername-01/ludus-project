from CTFd.utils.user import get_current_user

@ludus_bp.route("/challenges/<int:challenge_id>")
def challenge_info(challenge_id):
    user = get_current_user