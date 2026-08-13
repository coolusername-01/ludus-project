async function loadLudusInfo() {
    console.log("Ludus view.js loaded");

    const challengeId = challenge.data.id;
    console.log("Challenge ID:", challengeId);

    const response = await fetch(
        `/ludus_ranges/challenge/${challengeId}`
    );
