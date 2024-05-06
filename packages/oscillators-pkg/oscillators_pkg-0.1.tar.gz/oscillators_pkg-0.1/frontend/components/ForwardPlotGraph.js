import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js';

const ChartContainer = ({ chartRef, chartData, chartOptions, ariaLabel }) => {
  useEffect(() => {
    const chartInstance = new Chart(chartRef.current, {
      type: 'scatter',
      data: chartData,
      options: chartOptions,
    });

    return () => {
      chartInstance.destroy();
    };
  }, [chartRef, chartData, chartOptions]);

  return (
    <div className="relative h-[300px] w-[570px] bg-white rounded-lg">
      <canvas ref={chartRef} aria-label={ariaLabel}></canvas>
    </div>
  );
};

export default function Graph({ forward_r1, forward_lambda1, backward_r1, backward_lambda1 }) {
  const forwardR1Ref = useRef(null);
  const backwardR1Ref = useRef(null);

  const forwardR1ChartData = {
    datasets: [
      {
        data: forward_lambda1?.map((val, index) => ({ x: val, y: forward_r1[index] })),
        label: 'k1 vs r1 (Forward)',
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
        pointRadius: 5,
        pointHoverRadius: 8,
      },
    ],
  };

  const backwardR1ChartData = {
    datasets: [
      {
        data: backward_lambda1?.map((val, index) => ({ x: val, y: backward_r1[index] })),
        label: 'k1 vs r1 (Backward)',
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
        pointRadius: 5,
        pointHoverRadius: 8,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: {
        type: 'linear',
        position: 'bottom',
        title: {
          display: true,
          text: 'k1',
        },
        ticks: {
          color: 'white', // Add this line to make x-axis numbers white
        },
        grid: {
          color: 'white', // Make x-axis grid lines white
        },
      },
      y: {
        type: 'linear',
        position: 'left',
        title: {
          display: true,
          text: 'r1',
        },
        ticks: {
          color: 'white', // Add this line to make y-axis numbers white
        },
        grid: {
          color: 'white', // Make x-axis grid lines white
        },
      },
    },
    plugins: {
      tooltip: {
        enabled: true,
        callbacks: {
          label: (context) => {
            const { parsed } = context;
            return `(${parsed.x.toFixed(2)}, ${parsed.y.toFixed(2)})`;
          },
        },
      },
    },
  };

  return (
    <div className="relative flex flex-col min-w-0 break-words w-full !overflow-hidden rounded bg-blueGray-700">
      <div className=" flex-auto my-4 overflow-hidden">
        <div className="grid grid-cols-2 ">
          <div className="border-0 border-white mx-2 rounded-md !text-white">
            <h2 className="text-white text-lg font-semibold ">R1 Case (Forward)</h2>
            <ChartContainer
              chartRef={forwardR1Ref}
              chartData={forwardR1ChartData}
              chartOptions={chartOptions}
              ariaLabel="Forward k1 vs r1"
            />
          </div>
          <div className="border-0 border-white mx-2 rounded-md !text-white">
            <h2 className="text-white text-lg font-semibold ">R1 Case (Backward)</h2>
            <ChartContainer
              chartRef={backwardR1Ref}
              chartData={backwardR1ChartData}
              chartOptions={chartOptions}
              ariaLabel="Backward k1 vs r1"
            />
          </div>
        </div>
      </div>
    </div>
  );
}