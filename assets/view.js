console.log("LUDUS VIEW.JS STARTED");

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


async function loadLudusInfo() {
    console.log("Ludus view.js loaded");

    // const challengeId = CTFd._internal.challenge.data.id;;
    // console.log("Challenge ID:", challengeId);
    // console.log("Challenge ID:", challengeId);

    try
    {
      const response = await fetch(
        //`/ludus_ranges/challenges/${challengeId}`
        `/ludus_ranges/challenges`
      );

      if (!response.ok) {
        rangeId.textContent = "Check back later";
        kaliIp.textContent = "Check back later";
        return;
      }
    
    
      console.log("FETCH COMPLETED");
      const data = await response.json();
      //console.log("rangeId:", data.range_id);
      //console.log("kaliIp:", data.kali_ip);
      document.getElementById("range-id").textContent = data.range_id;
      document.getElementById("kali-ip").textContent = data.kali_ip;
    }
    catch(error)
    {
      console.error("Failed to load Ludus information:", error);

      rangeId.textContent = "Check back later";
      kaliIp.textContent = "Check back later";
    }
  }
//ai generated render stuff?? 
const oldPostRender = CTFd._internal.challenge.postRender;

CTFd._internal.challenge.postRender = function () {
    if (oldPostRender) {
        oldPostRender();
    }

    loadLudusInfo();
};