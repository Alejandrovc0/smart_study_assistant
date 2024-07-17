let isRunning = false;
let timer;
let studyTime = 25 * 60; // Default 25 minutes
let breakTime = 5 * 60; // Default 5 minutes
let messageInterval, progressInterval;

function produceStudySchedule() {
    // Collect user input
    const topic = document.getElementById('study-topic').value;
    const studyTimeInput = document.getElementById('study-time').value;
    const breakTimeInput = document.getElementById('break-time').value;

    if (!topic) {
        alert("Please enter a topic.");
        return;
    }

    // Prepare the payload
    const payload = {
        topic: topic,
        studyTime: studyTimeInput,
        breakTime: breakTimeInput
    };

    // Show loading spinner
    toggleBar(true);

    // Send the data to the backend
    fetch('http://localhost:8000/smart_study_assistant', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        toggleBar(false);
        displayAgentOutput(data);
    })
    .catch(error => {
        console.error('Error:', error);
        toggleBar(false);
        displayAgentOutput({ error: 'Failed to generate study plan. Please try again.' });
    });
}

function displayAgentOutput(data) {
    if (data.path) {
        const link = document.createElement('a');
        link.href = data.path;
        link.textContent = "Access your schedule here";
        document.body.appendChild(link); // Append the link to the body or to a specific element in your page

        // New code to display the path in the designated container
        const schedulePathContainer = document.getElementById('agentOutput');
        if (schedulePathContainer) {
            schedulePathContainer.textContent = `Schedule path: ${data.path}`;
        }
    } else {
        console.error('Error: Schedule path not found');
    }
}

function toggleBar(show) {
    const loadbar = document.getElementById('loadbar');
    const waitingMessages = document.getElementById('waiting-messages');
    const messages = ["Searching for sources", "Filtering relevant information", "Producing Schedule", "Revising Schedule", "Creating Study Plan", "Finalizing Study Plan"];
    if (show) {
        let messageIndex = 0;
        waitingMessages.textContent = messages[messageIndex];
        loadbar.style.width = '0%';
        messageInterval = setInterval(() => {
            if (messageIndex < messages.length - 1) {
                messageIndex = (messageIndex + 1) % messages.length;
                waitingMessages.textContent = messages[messageIndex];
            } else {
                clearInterval(messageInterval);
            }
        }, 15000);
        let width = 0;
        progressInterval = setInterval(() => {
            if (width >= 100) {
                clearInterval(progressInterval);
            } else {
                width += 10;
                loadbar.style.width = `${width}%`;
            }
        }, 8000);
    } else {
        clearInterval(messageInterval); // Clear the message interval
        clearInterval(progressInterval); // Clear the progress interval
        loadbar.style.width = '100%'; // Instantly set the loading bar to 100%
        waitingMessages.textContent = "Ready!"; // Update the message to indicate readiness
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('produce-study-plan').addEventListener('click', produceStudySchedule);
    document.getElementById('study-time').addEventListener('change', updateTimersFromInput);
    document.getElementById('break-time').addEventListener('change', updateTimersFromInput);
});

function openTab(evt, tabName) {
    var i, tabcontent, tabbuttons;

    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    tabbuttons = document.getElementsByClassName("tab-button");
    for (i = 0; i < tabbuttons.length; i++) {
        tabbuttons[i].className = tabbuttons[i].className.replace(" active", "");
    }

    if (tabName === 'LiveAgentOutput') {
        const topic = document.getElementById('study-topic').value;
        if (!topic) {
            alert("Please enter a topic first.");
            return;
        }
    }

    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";

    if (tabName === 'PlanSchedule') {
        resetTimer();
    }
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
    studyTime = parseInt(document.getElementById('study-time').value) * 60;
    document.getElementById('timer').textContent = formatTime(studyTime);
    document.getElementById('start-pause-button').textContent = 'Start';
}

function updateTimersFromInput() {
    if (!isRunning) {
        studyTime = parseInt(document.getElementById('study-time').value) * 60;
        breakTime = parseInt(document.getElementById('break-time').value) * 60;
        document.getElementById('timer').textContent = formatTime(studyTime);
    }
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