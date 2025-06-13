const ctx = document.getElementById('graph');
main()

async function main(){

const APIdata = await getData(0);
console.log(APIdata);

const xyData = convertObjectToXY(APIdata.values);

const labelsList = Object.keys(APIdata.values);

const regressionValues = countRegVal(APIdata);

const mixedChart = new Chart(ctx, {
   data: {
        datasets: [{
            type: 'scatter',
            label: 'Dane historyczne',
            data: xyData
        }, {
            type: 'line',
            label: 'Regresja liniowa',
            data: regressionValues,
        }],
        labels: labelsList
    },
   options: {
   plugins: {
    title: {
      display: true,
      text: 'Wynagrodzenie brutto dla: ' + APIdata.Nazwa,
      font: {
        size: 16
      },
      padding: {
        top: 10,
        bottom: 30
      }
    }
  },
    ticks: {
      stepSize: 1 // show label every 5 units
    }
   }

});
}

async function getData(code){
    try {
        const response = await fetch(`http://127.0.0.1:5001/get_data/${code}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            const errorMessage = await response.text();
            throw new Error(errorMessage);
        }

        const data = await response.json();
        return data;


    } catch (error) {
        console.error('Błąd podczas pobierania danych:', error);
    }

};

function convertObjectToXY(obj) {
  return Object.entries(obj).map(([x, y]) => ({
    x: Number(x),  // Convert year string to number
    y: y           // Keep original value
  }));
}

function countRegVal(data){
    tab = [];
    args = Object.keys(data.values);
    console.log( args);
    args.forEach((x) => tab.push(data.a * x + data.b));

    return tab;
}