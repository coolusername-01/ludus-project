//ctfd premade view.js template
CTFd._internal.challenge.data = undefined;
// TODO: Remove in CTFd v4.0
CTFd._internal.challenge.renderer = null;
CTFd._internal.challenge.preRender = function() {};
// TODO: Remove in CTFd v4.0
CTFd._internal.challenge.render = null;
CTFd._internal.challenge.postRender = function() {};
CTFd._internal.challenge.submit = function(preview) {
  var challenge_id = parseInt(CTFd.lib.$("#challenge-id").val());
  var submission = CTFd.lib.$("#challenge-input").val();

  var body = {
    challenge_id: challenge_id,
    submission: submission
  };
  var params = {};
  if (preview) {
    params["preview"] = true;
  }

  return CTFd.api.post_challenge_attempt(params, body).then(function(response) {
    if (response.status === 429) {
      // User was ratelimited but process response
      return response;
    }
    if (response.status === 403) {
      // User is not logged in or CTF is paused.
      return response;
    }
    return response;
  });
};

//my ludus addition
async function loadLudusInfo() {
    console.log("Ludus view.js loaded");
    //don't run if just on the home page
    if (!window.location.hash) {
      return;
    }
    try
    {
      // const response = await fetch(
      //   //`/ludus_ranges/challenges/${challengeId}`
      //   `/ludus_ranges/challenges`
      // );
      // const hash = window.location.hash;
      // const challengeId = hash.split("-").pop();

      CTFd.lib.$("#challenge-id").val()
      const response = await fetch(
          `/ludus_ranges/challenges/${challengeId}`
      );
      if (!response.ok) {
          document.getElementById("kali-ip").textContent = "Check back later";
          return;
      }
      console.log("FETCH COMPLETED");
      const data = await response.json();
      document.getElementById("kali-ip").textContent = data.kali_ip;
    }
    catch(error)
    {
      console.error("Failed to load Ludus information:", error);
      kaliIp.textContent = "Check back later";
    }
  }


if (!CTFd._internal.challenge.ludusPostRenderInstalled) {
    CTFd._internal.challenge.ludusPostRenderInstalled = true;

    CTFd._internal.challenge.postRender = function () {
        loadLudusInfo();
    };
}
