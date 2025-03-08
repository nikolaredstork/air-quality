import React, { useEffect, useState } from "react";
import { fetchAQI, connectWebSocket } from "./api.ts";
import Gauge from "./components/Gauge.tsx";
import "./App.css"; // Import the new CSS file

const App: React.FC = () => {
    const [aqi, setAQI] = useState<number | null>(null);

    useEffect(() => {
        fetchAQI().then(setAQI);
        const socket = connectWebSocket(setAQI);
        return () => socket.close();
    }, []);

    return (
        <div className="container">
            <h1 className="title">🌍 Kvalitet vazduha u Bratuncu</h1>
            {aqi !== null ? (
                <div className="card">
                    <Gauge aqi={aqi} />
                    <p className="aqi-value">Trenutna vrednost PM2.5: <strong>{aqi}</strong></p>
                </div>
            ) : (
                <p className="loading">Prikupljanje podataka...</p>
            )}
        </div>
    );
};

export default App;

