import React from "react";
import { RadialBarChart, RadialBar, ResponsiveContainer } from "recharts";

interface GaugeProps {
    aqi: number;
}

const Gauge: React.FC<GaugeProps> = ({ aqi }) => {
    const getAQIColor = (aqi: number) => {
        if (aqi <= 50) return "#00e400";  // Green (Good)
        if (aqi <= 100) return "#ffff00"; // Yellow (Moderate)
        if (aqi <= 150) return "#ff7e00"; // Orange (Unhealthy for Sensitive Groups)
        if (aqi <= 200) return "#ff0000"; // Red (Unhealthy)
        if (aqi <= 300) return "#8f3f97"; // Purple (Very Unhealthy)
        return "#7e0023";                 // Maroon (Hazardous)
    };

    return (
        <ResponsiveContainer width="100%" height={200}>
            <RadialBarChart
                cx="50%"
                cy="50%"
                innerRadius="80%"
                outerRadius="100%"
                barSize={20}
                data={[{ value: aqi, fill: getAQIColor(aqi) }]}
                startAngle={180}
                endAngle={0}
            >
                <RadialBar dataKey="value" {...({} as any)} />
            </RadialBarChart>
        </ResponsiveContainer>
    );
};

export default Gauge;
