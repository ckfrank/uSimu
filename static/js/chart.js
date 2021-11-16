// window:load event for Javascript to run after HTML
// because this Javascript is injected into the document head
window.addEventListener('load', function () {
    // Javascript code to execute after DOM content

    // full ZingChart schema can be found here:
    // https://www.zingchart.com/docs/api/json-configuration/
    var success = parseInt(document.getElementById('success-count').value);
    var pending = parseInt(document.getElementById('pending-count').value);
    var fail = parseInt(document.getElementById('fail-count').value);
    var warning = parseInt(document.getElementById('warning-count').value);

    const myConfig = {
        type: 'pie',
        legend: {
            draggable: true,
        },

        plot: {
            borderColor: "#2B313B",
            borderWidth: 3,
            // slice: 90,
            valueBox: {
                placement: 'out',
                text: '%t: %v\n%npv%',
            },
            tooltip: {
                fontSize: '18',
                padding: "5 10",
                text: "%npv%"
            },
            animation: {
                effect: 2,
                method: 5,
                speed: 900,
                sequence: 1,
                delay: 200
            }
        },
        title: {
            fontColor: "#434a4e",
            text: 'Your Overall Status',
            align: "left",
            fontSize: 25
        },
        // subtitle: {
        //     offsetX: 10,
        //     offsetY: 10,
        //     fontColor: "#8e99a9",
        //     fontSize: "16",
        //     text: 'May 2016',
        //     align: "left"
        // },
        plotarea: {
            margin: "45 0 0 0"
        },
        series: [
            {
                values: [success],
                text: "Success",
                backgroundColor: '#6FB07F',
            },
            {
                values: [fail],
                text: "Fail",
                backgroundColor: '#FF7965',
                detached: true
            },
            {
                values: [warning],
                text: 'Warning',
                backgroundColor: '#FFCB45',
                detached: true
            },
            {
                text: 'Pending',
                values: [pending],
                backgroundColor: '#747485',
                detached: true
            },

        ]
    };

    // render chart with width and height to
    // fill the parent container CSS dimensions
    zingchart.render({
        id: 'myChart',
        data: myConfig,
        height: '100%',
        width: '100%'
    });
});
