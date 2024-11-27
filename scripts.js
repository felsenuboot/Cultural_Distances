document.addEventListener("DOMContentLoaded", () => {
    // Elements and Global Variables
    const dataTable = $("#data-table").DataTable();
    const datasetSelector = document.getElementById("dataset-selector");
    const countrySelector1 = document.getElementById("country-selector-1");
    const countrySelector2 = document.getElementById("country-selector-2");
    const visualizationCanvas = document.getElementById("visualization-canvas").getContext("2d");
    let chartInstance = null;

    let hofstedeData = [];
    let cultureMapData = [];

    // Load Data
    function loadData() {
        Promise.all([
            fetch("data/hofstede_data.json").then(res => res.json()),
            fetch("data/culture_map_data.json").then(res => res.json()),
        ])
            .then(([hofstede, cultureMap]) => {
                hofstedeData = hofstede;
                cultureMapData = cultureMap;
                populateTable(hofstedeData);
                populateCountrySelectors(hofstedeData);
            })
            .catch(err => console.error("Error loading data:", err));
    }

    // Populate Table
    function populateTable(data) {
        dataTable.clear();
        data.forEach(country => {
            Object.entries(country.scores).forEach(([dimension, value]) => {
                dataTable.row.add([country.name, dimension, value]);
            });
        });
        dataTable.draw();
    }

    // Populate Country Selectors
    function populateCountrySelectors(data) {
        countrySelector1.innerHTML = data.map(c => `<option value="${c.name}">${c.name}</option>`).join("");
        countrySelector2.innerHTML = data.map(c => `<option value="${c.name}">${c.name}</option>`).join("");
    }

    // Compare Countries
    function compareCountries() {
        const country1 = countrySelector1.value;
        const country2 = countrySelector2.value;

        if (!country1 || !country2) {
            alert("Please select two countries.");
            return;
        }

        const data1 = hofstedeData.find(c => c.name === country1) || {};
        const data2 = hofstedeData.find(c => c.name === country2) || {};
        const cultureData1 = cultureMapData.find(c => c.name === country1) || {};
        const cultureData2 = cultureMapData.find(c => c.name === country2) || {};

        const comparisonData = [
            ...Object.entries(data1.scores || {}),
            ...Object.entries(cultureData1.scores || {}),
        ].map(([dim, val], i) => [dim, val, (data2.scores || {})[dim] || "N/A"]);

        const table = document.getElementById("comparison-table");
        table.innerHTML = `<thead>
            <tr>
                <th>Dimension</th>
                <th>${country1}</th>
                <th>${country2}</th>
            </tr>
        </thead>
        <tbody>
            ${comparisonData.map(([dim, val1, val2]) => `
                <tr>
                    <td>${dim}</td>
                    <td>${val1}</td>
                    <td>${val2}</td>
                </tr>`).join("")}
        </tbody>`;
    }

    // Generate Visualizations
    function generateVisualization() {
        const selectedType = document.getElementById("visualization-selector").value;

        if (chartInstance) chartInstance.destroy();

        const labels = hofstedeData.map(c => c.name);
        const data = hofstedeData.map(c => c.scores["Individualism"] || 0);

        chartInstance = new Chart(visualizationCanvas, {
            type: selectedType === "boxplot" ? "bar" : "scatter",
            data: {
                labels,
                datasets: [
                    {
                        label: "Individualism Scores",
                        data,
                        backgroundColor: "rgba(75, 192, 192, 0.2)",
                        borderColor: "rgba(75, 192, 192, 1)",
                        borderWidth: 1,
                    },
                ],
            },
            options: {
                responsive: true,
                title: { display: true, text: "Visualization" },
                scales: { y: { beginAtZero: true } },
            },
        });
    }

    // Event Listeners
    datasetSelector.addEventListener("change", () => {
        const selectedData = datasetSelector.value === "hofstede" ? hofstedeData : cultureMapData;
        populateTable(selectedData);
        populateCountrySelectors(selectedData);
    });

    document.getElementById("compare-countries").addEventListener("click", compareCountries);
    document.getElementById("generate-visualization").addEventListener("click", generateVisualization);

    // Initial Load
    loadData();
});