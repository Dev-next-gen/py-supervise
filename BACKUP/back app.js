import React, { useEffect, useState } from "react";
import { Card, CardContent, Typography, Grid } from "@mui/material";
import { Line } from "react-chartjs-2";
import "./App.css";
import "core-js/stable";
import "regenerator-runtime/runtime";

function App() {
  const [resources, setResources] = useState({});
  const [tasks, setTasks] = useState([]);
  const [timestamps, setTimestamps] = useState([]);
  const [cpuUsage, setCpuUsage] = useState([]);
  const [memoryUsage, setMemoryUsage] = useState([]);

  useEffect(() => {
    const eventSource = new EventSource("http://127.0.0.1:8000/monitoring");

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        setResources(data.resources || {});
        setTasks(data.tasks || []);

        setTimestamps((prev) => [
          ...prev,
          new Date(data.timestamp).toLocaleTimeString(),
        ]);
        setCpuUsage((prev) => [...prev, data.resources?.cpu_usage || 0]);
        setMemoryUsage((prev) => [...prev, data.resources?.memory_usage || 0]);
      } catch (error) {
        console.error("Error parsing data from monitoring endpoint:", error);
      }
    };

    eventSource.onerror = () => {
      console.error("Connection to monitoring endpoint lost.");
      eventSource.close();
    };

    return () => eventSource.close();
  }, []);

  const chartData = {
    labels: timestamps,
    datasets: [
      {
        label: "CPU Usage (%)",
        data: cpuUsage,
        fill: false,
        borderColor: "rgba(75,192,192,1)",
        tension: 0.1,
      },
      {
        label: "Memory Usage (%)",
        data: memoryUsage,
        fill: false,
        borderColor: "rgba(255,99,132,1)",
        tension: 0.1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        display: true,
        position: "top",
      },
    },
  };

  return (
    <div style={{ padding: "20px" }}>
      <Typography variant="h4" gutterBottom>
        Monitoring Dashboard
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6">CPU Usage</Typography>
              <Typography variant="h4">
                {resources.cpu_usage || 0}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6">Memory Usage</Typography>
              <Typography variant="h4">
                {resources.memory_usage || 0}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6">GPU Memory Free</Typography>
              <Typography variant="h4">
                {resources.gpu_memory_free
                  ? (resources.gpu_memory_free / 1024 ** 2).toFixed(2)
                  : 0}{" "}
                MB
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Typography variant="h5" style={{ marginTop: "20px" }}>
        Active Tasks
      </Typography>
      <ul>
        {tasks.map((task, index) => (
          <li key={index}>
            Task ID: {task.task_id} | Status: {task.status} | Result:{" "}
            {task.result || "N/A"}
          </li>
        ))}
      </ul>

      <Typography variant="h5" style={{ marginTop: "20px" }}>
        Resource Usage Over Time
      </Typography>
      <Line data={chartData} options={chartOptions} />
    </div>
  );
}

export default App;
