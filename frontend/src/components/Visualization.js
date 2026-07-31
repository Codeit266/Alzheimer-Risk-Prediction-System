import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from "chart.js";

import { Bar } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function Visualization({ features }) {

  if (!features) {
    return <p className="screenText">Loading feature visualization...</p>;
  }

  const labels = Object.keys(features).map(key => 
    key.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase())
  );

  const data = {
    labels: labels,
    datasets: [
      {
        label: "Feature Values",
        data: Object.values(features),
        backgroundColor: "#111111",
        borderColor: "#000000",
        borderWidth: 1,
        borderRadius: 0,
        borderSkipped: false,
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    layout: {
      padding: {
        bottom: 12,
        top: 4,
        left: 4,
        right: 4
      }
    },
    plugins: {
      legend: {
        display: true,
        position: 'top',
        labels: {
          color: '#111111',
          font: {
            family: "'Plus Jakarta Sans', sans-serif",
            size: 12,
            weight: '600'
          }
        }
      },
      tooltip: {
        backgroundColor: 'rgba(34, 20, 50, 0.95)',
        titleColor: '#fff',
        bodyColor: '#fff',
        borderColor: 'rgba(255, 255, 255, 0.1)',
        borderWidth: 1,
        padding: 12,
        cornerRadius: 8,
        displayColors: false,
        titleFont: {
          family: "'Plus Jakarta Sans', sans-serif",
          weight: '600'
        },
        bodyFont: {
          family: "'Plus Jakarta Sans', sans-serif"
        }
      }
    },
    scales: {
      y: {
        grid: {
          color: 'rgba(107, 63, 160, 0.12)',
          drawBorder: false,
        },
        ticks: {
          color: '#3A2257',
          font: {
            family: "'Plus Jakarta Sans', sans-serif",
            size: 11
          }
        }
      },
      x: {
        grid: {
          display: false
        },
        ticks: {
          color: '#3A2257',
          maxRotation: 45,
          minRotation: 45,
          font: {
            family: "'Plus Jakarta Sans', sans-serif",
            size: 10,
            weight: '500'
          }
        }
      }
    }
  };

  return (
    <div className="chartBox" style={{ height: "100%", display: "flex", flexDirection: "column", boxSizing: "border-box" }}>
      <span className="sectionCategory">Feature Analysis</span>
      <h3 className="chartTitle" style={{ marginBottom: "15px" }}>
        Speech Feature Analysis
      </h3>
      <div style={{ position: "relative", minHeight: "190px", height: "100%", width: "100%", flexGrow: 1 }}>
        <Bar data={data} options={options} />
      </div>
    </div>
  );
}

export default Visualization;