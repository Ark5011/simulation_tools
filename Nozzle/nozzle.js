document.addEventListener('DOMContentLoaded', function() {
    var selectTd = document.getElementById('td_orificeNumber');
    var tdOrificeNum = [34, 37, 40, 43, 46, 49, 52, 55, 58, 61, 62, 64, 66, 67, 68, 70, 73, 75, 76, 80, 82, 85, 86, 88, 90, 91, 94, 97, 100, 103, 106, 109, 112, 115, 118, 121, 127, 133, 136, 142, 145, 148, 151, 154, 157];

    tdOrificeNum.forEach(function(value) {
        var option = document.createElement('option');
        option.value = value;
        option.textContent = value;
        selectTd.appendChild(option);
    });

    var selectTdl = document.getElementById('tdl_orificeNumber');
    var tdlOrificeNum = [18, 20, 22, 24, 27, 30, 33, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58];

    tdlOrificeNum.forEach(function(value) {
        var option = document.createElement('option');
        option.value = value;
        option.textContent = value;
        selectTdl.appendChild(option);
    });

    var form = document.getElementById('nozzleForm');
    var calculateTdButton = document.getElementById('calculateTdButton');
    var calculateTdlButton = document.getElementById('calculateTdlButton');
    var formulachartButtonContainer = document.getElementById('formulachartButtonContainer');

    function showGenerateExcelButton() {
        formulachartButtonContainer.style.display = 'block';
    }

    calculateTdButton.addEventListener('click', function() {
        var formData = new FormData(form);
        var formDataJson = {};

        for (var pair of formData.entries()) {
            if (!pair[0].startsWith('tdl_')) {
                formDataJson[pair[0]] = pair[1];
            }
        }

        console.log('TD Form Data:', formDataJson);

        fetch('/td', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formDataJson)
        })
        .then(response => response.json())
        .then(data => {
            console.log('TD Response Data:', data);

            document.querySelector('[data-field="td_liquid_flow_rate"]').textContent = data.td_liquid_flow_rate;
            document.querySelector('[data-field="td_spray_angle"]').textContent = data.td_spray_angle;
            document.querySelector('[data-field="td_droplet_size"]').textContent = data.td_droplet_size;
            document.querySelector('[data-field="td_powder_flow_rate"]').textContent = data.td_powder_flow_rate;

            showGenerateExcelButton();
        })
        .catch(error => console.error('Error:', error));
    });

    calculateTdlButton.addEventListener('click', function() {
        var formData = new FormData(form);
        var formDataJson = {};

        for (var pair of formData.entries()) {
            if (!pair[0].startsWith('td_')) {
                formDataJson[pair[0]] = pair[1];
            }
        }

        console.log('TDL Form Data:', formDataJson);

        fetch('/tdl', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formDataJson)
        })
        .then(response => response.json())
        .then(data => {
            console.log('TDL Response Data:', data);

            document.querySelector('[data-field="tdl_liquid_flow_rate"]').textContent = data.tdl_liquid_flow_rate;
            document.querySelector('[data-field="tdl_powder_flow_rate"]').textContent = data.tdl_powder_flow_rate;

            showGenerateExcelButton();
        })
        .catch(error => console.error('Error:', error));
    });

    document.getElementById("generateexcelButton").addEventListener("click", function(event) {
        event.preventDefault();

        const formData = new FormData(form);

        fetch('/generate_excel', {
            method: 'POST',
            body: formData
        })
        .then(response => response.blob())
        .then(blob => {
            const link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = 'nozzle.xlsx';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        })
        .catch(error => console.error('Error:', error));
    });
});