document.addEventListener("DOMContentLoaded", function () {
    // Initialize the map
    const map = L.map('map').setView([20.5937, 78.9629], 5); // Centered on India

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // Fetch map data
    fetch("/map-data")
        .then(response => response.json())
        .then(data => {
            if (!data || data.length === 0) {
                console.error("No data available to display on the map.");
                return;
            }

            // Prepare heatmap data
            const heatmapData = data.map(point => [
                point.latitude,
                point.longitude,
                point.current_infected / 1000 // Adjust intensity scale
            ]);

            // Add heatmap layer
            const heatmapLayer = L.heatLayer(heatmapData, {
                radius: 20,
                blur: 15,
                maxZoom: 17,
                gradient: {
                    0.2: 'blue',
                    0.4: 'lime',
                    0.6: 'yellow',
                    1: 'red'
                }
            }).addTo(map);

            // Add markers for individual locations
            data.forEach(point => {
                const { latitude, longitude, location, current_infected } = point;
                L.marker([latitude, longitude])
                    .addTo(map)
                    .bindPopup(`<strong>${location}</strong><br>Current Infected: ${current_infected}`);
            });
        })
        .catch(error => console.error("Error fetching map data:", error));

    // Notifications
    requestNotificationPermission();

    // Example notification
    setTimeout(() => {
        sendNotification(
            "Epidemic Alert",
            "High-risk outbreak detected in Bangalore. Avoid crowded areas."
        );
    }, 5000); // Delay for demonstration
});

// Function to check and request notification permissions
function requestNotificationPermission() {
    if ('Notification' in window) {
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                console.log("Notifications enabled.");
                sendNotification("Welcome!", "You will now receive updates about epidemic outbreaks.");
            } else {
                console.log("Notifications not enabled.");
            }
        });
    } else {
        console.log("Browser does not support notifications.");
    }
}

// Function to send a notification
function sendNotification(title, body) {
    new Notification(title, {
        body: body,
        icon: "/static/images/notification-icon.png" // Add an appropriate icon
    });
}
