/**
 * Event Logger JavaScript
 * Handles audio feedback and event management for TRBD Clinical Trial
 */

let currentEvent = null;
let activeButton = null;
let audioContext = null;
let isBeeping = false;

// Initialize audio context on first user interaction
function initAudio() {
    if (!audioContext) {
        try {
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
            // Resume context in case it's suspended due to autoplay policy
            if (audioContext.state === 'suspended') {
                audioContext.resume();
            }
        } catch (error) {
            console.warn('Audio not available:', error);
            audioContext = null;
        }
    }
}

function playBeep() {
    // Prevent overlapping beeps
    if (isBeeping) return;

    initAudio();

    // Fallback if audio context is not available
    if (!audioContext) {
        console.warn('Audio context not available');
        return;
    }

    try {
        isBeeping = true;
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();

        oscillator.type = "sine";
        oscillator.frequency.setValueAtTime(1000, audioContext.currentTime);

        // Add volume control and fade out to prevent clicking
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);

        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);

        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.3);

        // Clean up after beep completes
        oscillator.onended = () => {
            isBeeping = false;
            oscillator.disconnect();
            gainNode.disconnect();
        };
    } catch (error) {
        console.warn('Error playing beep:', error);
        isBeeping = false;
    }
}

function getNotes() {
    return document.getElementById("notes").value;
}

function toggleEvent(eventName, button) {
    // Initialize audio on first user interaction
    initAudio();

    fetch('/toggle_event', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 'event': eventName, 'notes': getNotes() })
    }).then(response => response.json())
        .then(data => {
            document.getElementById("status").innerText = data.status;
            if (activeButton && activeButton !== button) {
                activeButton.classList.remove('active');
            }
            if (data.active_event === null) {
                button.classList.remove('active');
                document.getElementById("notes").value = "";
            } else {
                button.classList.add('active');
                activeButton = button;
            }
            currentEvent = data.active_event;
            playBeep();
        })
        .catch(error => {
            console.error('Error toggling event:', error);
        });
}

function abortEvent() {
    if (!currentEvent) {
        alert("No active event to abort.");
        return;
    }

    // Initialize audio on first user interaction
    initAudio();

    fetch('/abort_event', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 'notes': getNotes() })
    }).then(response => response.json())
        .then(data => {
            document.getElementById("status").innerText = data.status;
            if (activeButton) activeButton.classList.remove('active');
            currentEvent = data.active_event;
            document.getElementById("notes").value = "";
            playBeep();
        })
        .catch(error => {
            console.error('Error aborting event:', error);
        });
}
