// plot.worker.js
export default function plotWorker() {
    self.onmessage = function (e) {
        console.log(e)
      const { x, data, xlabel, ylabel, graphLabel } = e.data;
  
      function randomColor() {
        return "#" + Math.floor(Math.random() * 16777215).toString(16);
      }
  
      const chartData = {
        datasets: [
          {
            data: x.map((ele, index) => ({ x: ele, y: data[index] })),
            label: graphLabel || "Scatter Plot",
            borderColor: randomColor(),
            backgroundColor: randomColor(),
            fill: false,
            pointRadius: 3,
            pointHoverRadius: 8,
          },
        ],
      };
  
      self.postMessage({ chartData });
    };
  }
  