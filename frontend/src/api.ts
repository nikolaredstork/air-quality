import axios from "axios";

const API_URL = "http://localhost:8000"; // Update this for production

export const fetchAQI = async () => {
    const response = await axios.get(`${API_URL}/aqi`);
    return response.data.aqi;
};

export const connectWebSocket = (onUpdate: (aqi: number) => void) => {
    const socket = new WebSocket(`${API_URL.replace("http", "ws")}/ws`);
    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.aqi !== null) onUpdate(data.aqi);
    };
    return socket;
};

