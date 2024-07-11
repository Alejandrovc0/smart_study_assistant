function generateStudyPlan() {
        var topic = document.getElementById('study-form').value.trim();
        if (topic === '') {
            alert('Please fill in your topic.');
            return;
        }

    fetch('http://localhost:8000/smart_study_assistant', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        toggleLoading(false);
        displayNewspaper(data);
    })
    .catch((error) => {
        toggleLoading(false);
        console.error('Error:', error);
    });
}

function toggleLoading(isLoading) {
    const loadingSection = document.getElementById('loading');
    const loadingMessages = document.getElementById('loadingMessages');
    const messages = ["Looking for news...", "Curating sources...", "Writing articles...", "Editing final newspaper..."];
    loadingMessages.style.fontFamily = "'Gill Sans', sans-serif";
    if (isLoading) {
        loadingSection.classList.remove('hidden');
        let messageIndex = 0;
        loadingMessages.textContent = messages[messageIndex];
        const interval = setInterval(() => {
            if (messageIndex < messages.length - 1) {
                messageIndex++;
                loadingMessages.textContent = messages[messageIndex];
            } else {
                clearInterval(interval);
            }
        }, 12000);
        loadingSection.dataset.intervalId = interval;
    } else {
        loadingSection.classList.add('hidden');
        clearInterval(loadingSection.dataset.intervalId);
    }
}


let topicCount = 1;

window.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('produceNewspaper').addEventListener('click', produceNewspaper);
    document.querySelectorAll('.layout-icon').forEach(icon => {
        icon.addEventListener('click', selectLayout);
    });
    addIconToLastTopic();
});

function addIconToLastTopic() {
    // Remove icons from all topics
    document.querySelectorAll('.add-topic, .remove-topic').forEach(icon => {
        icon.remove();
    });

    // Add icons to the last topic only
    const lastTopic = document.getElementById('topicGroup' + topicCount);
    if (lastTopic) {
        const addIcon = document.createElement('span');
        addIcon.className = 'icon add-topic';
        addIcon.textContent = '+';
        addIcon.addEventListener('click', addTopicField);
        lastTopic.appendChild(addIcon);

        if (topicCount > 1) {
            const removeIcon = document.createElement('span');
            removeIcon.className = 'icon remove-topic';
            removeIcon.textContent = '-';
            removeIcon.addEventListener('click', removeTopicField);
            lastTopic.appendChild(removeIcon);
        }
    }
}

function addTopicField() {
    topicCount++;
    const formGroup = document.createElement('div');
    formGroup.className = 'form-group';
    formGroup.id = 'topicGroup' + topicCount;

    const inputElement = document.createElement('input');
    inputElement.type = 'text';
    inputElement.id = 'topic' + topicCount;
    inputElement.name = 'topic' + topicCount;
    inputElement.className = 'inputText';
    inputElement.required = true;

    formGroup.appendChild(inputElement);

    document.getElementById('topicForm').appendChild(formGroup);

    addIconToLastTopic();
}


function removeTopicField(event) {
    const topicGroup = event.target.parentElement;
    if (topicGroup && topicGroup.id !== 'topicGroup1') {
        topicGroup.remove();
        topicCount--;
        addIconToLastTopic();
    }
}

function displayNewspaper(data) {
    if (data.path) {
        window.location.href = data.path;
    } else {
        console.error('Error: Newspaper path not found');
    }
}