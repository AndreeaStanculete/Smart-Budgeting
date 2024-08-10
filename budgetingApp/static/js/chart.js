function getLineChart(labels, data) {
    var [dataI, dataE] = data;
    console.log(dataI);

    return {
        type: "line",
        data: {
            labels: labels,
            datasets: [{ 
                data: dataI,
                borderColor: '#C03D3D',
                fill: false,
                label: "Incomes"
            }, { 
                data: dataE,
                borderColor: '#6CA697',
                fill: false,
                label: "Expenses"
            }]
        },
        options: {
            legend: {display: true}
        }
    };
}

function getBarChart(labels, data) {
    return {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                backgroundColor: [
                '#C03D3D', '#6CA697', '#5E81BF', '#CD88D1', '#4E7359', '#1C5273', '#94344D', '#dcedc1', '#66b2b2',
                '#66545e', '#aa6f73', '	#eea990', '#7289da', '#a39193', '#abb1cf', '#dec2cb', '#4b86b4', '#adcbe3',
                '#777696', '#1f493d', '#423629', '#5b7c99', '#f1c27d', '#ebdada', '#dfdfde'
                ],
                data: data
            }]
        },
        options: {
            legend: {display: false},
            title: {
                display: true,
            }
        }
    };
}

function getPieChart(labels, data) {
    return {
        type: 'pie',
        data: {
            datasets: [{
                data: data,
                backgroundColor: [
                    '#C03D3D', '#6CA697', '#5E81BF', '#CD88D1', '#4E7359', '#1C5273', '#94344D', '#dcedc1', '#66b2b2',
                    '#66545e', '#aa6f73', '	#eea990', '#7289da', '#a39193', '#abb1cf', '#dec2cb', '#4b86b4', '#adcbe3',
                    '#777696', '#1f493d', '#423629', '#5b7c99', '#f1c27d', '#ebdada', '#dfdfde'
                ],
                label: 'Population'
            }],
            labels: labels
        },
        options: {
            legend: {
                display: false
            },
            responsive: true,
            position: 'right',
            align: 'end'
        }
    };
}

function drawChart(type, chart, labels, data) {
    var ctx = document.getElementById(chart).getContext('2d');
    var config;

    switch (type) {
        case 0:
            config = getLineChart(labels, data);
            break;
        case 1:
            config = getBarChart(labels, data);
            break;
        default:
            config = getPieChart(labels, data);
            break;
    }

    window.myPie = new Chart(ctx, config);
}