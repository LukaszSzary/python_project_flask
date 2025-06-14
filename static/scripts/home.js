const ctx = document.getElementById('graph');

fillCitySelectLList();

let mixedChart = undefined;

async function main(code = 0) {


  const APIdata = await getData(code);

  const xyData = convertObjectToXY(APIdata.values);
  const labelsList = Object.keys(APIdata.values);
  const regressionValues = countRegVal(APIdata);


  if (mixedChart !== undefined) {
    mixedChart.destroy(); // Destroy the previous chart instance if it exists
  }

  mixedChart = new Chart(ctx, {
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
      },
      scales: {
        x: {
          type: 'category', // <--- KLUCZOWA ZMIANA
          title: {
            display: true,
            text: 'Rok'
          }
        },
        y: {
          title: {
            display: true,
            text: 'Wynagrodzenie'
          }
        }

      }
    }
  });
}

async function getData(code) {
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

async function getCity() {
  try {
    const response = await fetch(`http://127.0.0.1:5001/get_codes/`, {
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

function countRegVal(data) {
  tab = [];
  args = Object.keys(data.values);

  args.forEach((x) => tab.push(data.a * x + data.b));

  return tab;
}


async function fillCitySelectLList() {

  const select = document.getElementById('menu');
  const cityData = await getCity();

  // Generowanie opcji
  cityData.forEach(city => {
    const option = document.createElement('option');

    option.textContent = city['Nazwa'];
    option.value = city['Kod'];
    select.appendChild(option);
  });
  main(0);
  // Przejście do wybranej strony po zmianie
  select.addEventListener('change', function () {
    const wybranyLink = this.value;
    if (wybranyLink) {
      main(wybranyLink);
    }
  });
}