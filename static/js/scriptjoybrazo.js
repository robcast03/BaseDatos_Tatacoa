
// Función para actualizar el valor del input numérico y la variable correspondiente
function updateNumberInput(slider) {
    const id = slider.id;
    const numberInput = document.getElementById(id.replace('grado', 'angulo').replace('VELOCIDAD', 'vel').replace('referen','Referencia'));
    numberInput.value = slider.value;
    
    // Actualizar la variable correspondiente utilizando window[id]
    window[id.replace('grado', 'angulo').replace('VELOCIDAD', 'vel').replace('referen','Referencia')]= parseInt(slider.value);
    sendDataToPython();
}

function increaseFirstSliderValue() {
    const Slider = document.getElementById('grado1');
    const currentValue = parseInt(Slider.value);
    if (!isNaN(currentValue)) {
        Slider.value = currentValue + 1;
        updateNumberInput(Slider);
        sendDataToPython(); // Llamar a la función para enviar los datos a Python
    }
}
function increaseSecondSliderValue() {
    const Slider = document.getElementById('grado2');
    const currentValue = parseInt(Slider.value);
    if (!isNaN(currentValue)) {
        Slider.value = currentValue + 1;
        updateNumberInput(Slider);
        sendDataToPython(); // Llamar a la función para enviar los datos a Python
    }
}
function increaseThirdSliderValue() {
    const Slider = document.getElementById('grado3');
    const currentValue = parseInt(Slider.value);
    if (!isNaN(currentValue)) {
        Slider.value = currentValue + 1;
        updateNumberInput(Slider);
        sendDataToPython(); // Llamar a la función para enviar los datos a Python
    }
}
function increaseFourthSliderValue() {
    const Slider = document.getElementById('grado4');
    const currentValue = parseInt(Slider.value);
    if (!isNaN(currentValue)) {
        Slider.value = currentValue + 1;
        updateNumberInput(Slider);
        sendDataToPython(); // Llamar a la función para enviar los datos a Python
    }
}
function increaseFifthSliderValue() {
    const Slider = document.getElementById('grado5');
    const currentValue = parseInt(Slider.value);
    if (!isNaN(currentValue)) {
        Slider.value = currentValue + 1;
        updateNumberInput(Slider);
        sendDataToPython(); // Llamar a la función para enviar los datos a Python
    }
}
    function decreaseFirstSliderValue() {
        const Slider = document.getElementById('grado1');
        const currentValue = parseInt(Slider.value);
        if (!isNaN(currentValue)) {
            Slider.value = currentValue - 1;
            updateNumberInput(Slider);
            sendDataToPython(); // Llamar a la función para enviar los datos a Python
        }
    }
    function decreaseSecondSliderValue() {
        const Slider = document.getElementById('grado2');
        const currentValue = parseInt(Slider.value);
        if (!isNaN(currentValue)) {
            Slider.value = currentValue - 1;
            updateNumberInput(Slider);
            sendDataToPython(); // Llamar a la función para enviar los datos a Python
        }
    }
    function decreaseThirdSliderValue() {
        const Slider = document.getElementById('grado3');
        const currentValue = parseInt(Slider.value);
        if (!isNaN(currentValue)) {
            Slider.value = currentValue - 1;
            updateNumberInput(Slider);
            sendDataToPython(); // Llamar a la función para enviar los datos a Python
        }
    }
    function decreaseFourthSliderValue() {
        const Slider = document.getElementById('grado4');
        const currentValue = parseInt(Slider.value);
        if (!isNaN(currentValue)) {
            Slider.value = currentValue - 1;
            updateNumberInput(Slider);
            sendDataToPython(); // Llamar a la función para enviar los datos a Python
        }
    }
    function decreaseFifthSliderValue() {
        const Slider = document.getElementById('grado5');
        const currentValue = parseInt(Slider.value);
        if (!isNaN(currentValue)) {
            Slider.value = currentValue - 1;
            updateNumberInput(Slider);
            sendDataToPython(); // Llamar a la función para enviar los datos a Python
        }
    }

document.addEventListener('keydown', function(event) {
    if (event.key === 'q') {
        increaseFirstSliderValue();
    }
    if (event.key === 'w') {
        window.movimiento = 2;
        increaseSecondSliderValue();
    }
    if (event.key === 'e') {
        increaseThirdSliderValue();
    }
    if (event.key === 'r') {
        increaseFourthSliderValue();
    }
    if (event.key === 'v') {
        increaseFifthSliderValue();
    }
    if (event.key === 'p') {
        decreaseFirstSliderValue();
    }
    if (event.key === 'o') {
        window.movimiento = 2;
        decreaseSecondSliderValue();
    }
    if (event.key === 'i') {
        decreaseThirdSliderValue();
    }
    if (event.key === 'u') {
        decreaseFourthSliderValue();
    }
    if (event.key === 'b') {
        decreaseFifthSliderValue();
    }
});


function updateSliderFromNumberInput(numberInput) {
    const id = numberInput.id;
    const slider = document.getElementById(id.replace('angulo', 'grado').replace('vel', 'VELOCIDAD').replace('Referencia','referen'));

    // Actualizar el valor del slider cuando se cambie el cuadro de entrada
    slider.value = parseInt(numberInput.value);

    // Actualizar la variable correspondiente utilizando window[id]
    //window[id.replace('angulo', 'grado').replace('vel', 'VELOCIDAD').replace('Referencia','referen')] = parseInt(numberInput.value);
    const variableName = id.replace('angulo', 'grado').replace('vel', 'VELOCIDAD').replace('Referencia','referen');
    window[variableName] = parseInt(numberInput.value);

    // Igualar angulo1 con grado1
    if (variableName === 'grado1') {
        window['angulo1'] = parseInt(numberInput.value);
    }

    sendDataToPython(); // Llamar a la función para enviar los datos a Python
}

// Agregar eventos de escucha al cuadro de entrada de número
const numberInputs = document.querySelectorAll('.cuadro');
numberInputs.forEach(numberInput => {
    numberInput.addEventListener('change', function() {
        updateSliderFromNumberInput(numberInput);

    });
});
// Seleccionar todos los sliders
const sliders = document.querySelectorAll('.slider');

// Agregar event listener a cada slider
sliders.forEach(slider => {
    slider.addEventListener('input', () => {
        updateNumberInput(slider);

         // Llamar a la función para enviar los datos a Python
    });
});

function sendDataToPython() {
    // Crear un objeto con los valores de los ángulos y velocidades
    const data = {
        angulo1: parseFloat(window.angulo1),
        angulo2: parseFloat(window.angulo2),
        angulo3: parseFloat(window.angulo3),
        angulo4: parseFloat(window.angulo4),
        angulo5: parseFloat(window.angulo5),
        angulo6: parseFloat(window.angulo6),
        angulo7: parseFloat(window.angulo7),
        vel1: parseFloat(window.vel1),
        vel2: parseFloat(window.vel2),
        vel3: parseFloat(window.vel3),
        vel4: parseFloat(window.vel4),
        vel5: parseFloat(window.vel5),
        vel6: parseFloat(window.vel6),
        vel7: parseFloat(window.vel7),
        ref: parseFloat(window.Referencia)
    };

    console.log(data);

    // Enviar los datos al servidor Flask
    fetch('/receive_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
}
