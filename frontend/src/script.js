function produceStudySchedule() {
    // Placeholder function to produce study schedule
    var topics = [];

    // Get the topics from the user
    var topics = document.getElementById("stuidy-topic").value;

    if (topics == "") {
        alert("Please enter the topics you want to study.");
        return;
    }
    console.log(topics);


}























let timer;
let isRunning = false;
let studyTime = 25 * 60; // in seconds

function openTab(evt, tabName) {
    let i, tabcontent, tabbuttons;

    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    tabbuttons = document.getElementsByClassName("tab-button");
    for (i = 0; i < tabbuttons.length; i++) {
        tabbuttons[i].className = tabbuttons[i].className.replace(" active", "");
    }

    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

function generateStudyPlan() {
    // Placeholder function to generate study plan
    console.log("Generating study plan...");
}

function startPauseTimer() {
    if (isRunning) {
        clearInterval(timer);
        document.getElementById('start-pause-button').textContent = 'Start';
    } else {
        timer = setInterval(updateTimer, 1000);
        document.getElementById('start-pause-button').textContent = 'Pause';
    }
    isRunning = !isRunning;
}

function resetTimer() {
    clearInterval(timer);
    isRunning = false;
    studyTime = 25 * 60;
    document.getElementById('timer').textContent = formatTime(studyTime);
    document.getElementById('start-pause-button').textContent = 'Start';
}

function updateTimer() {
    if (studyTime > 0) {
        studyTime--;
        document.getElementById('timer').textContent = formatTime(studyTime);
    } else {
        clearInterval(timer);
        isRunning = false;
        document.getElementById('start-pause-button').textContent = 'Start';
    }
}

function formatTime(seconds) {
    let mins = Math.floor(seconds / 60);
    let secs = seconds % 60;
    return `${mins < 10 ? '0' : ''}${mins}:${secs < 10 ? '0' : ''}${secs}`;
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('timer').textContent = formatTime(studyTime);
});
