let move;
// Función para actualizar el valor del input numérico y la variable correspondiente
function updateNumberInput(slider) {
    const id = slider.id;
    const numberInput = document.getElementById(id.replace('grado', 'angulo').replace('VELOCIDAD', 'vel').replace('referen','Referencia').replace('POSICIONX','posx').replace('POSICIONY','posy').replace('POSICIONZ','posz'));
    numberInput.value = slider.value;
    
    // Actualizar la variable correspondiente utilizando window[id]
    window[id.replace('grado', 'angulo').replace('VELOCIDAD', 'vel').replace('referen','Referencia').replace('POSICIONX','posx').replace('POSICIONY','posy').replace('POSICIONZ','posz')]= parseInt(slider.value);
}

document.addEventListener('keydown', function(event) {
    if (event.key === 'h') {
        move='h';
        console.log(move);
    }
    if (event.key === 'e') {
        move='e';
        console.log(move);
        sendDataToPython();
    }
});


function updateSliderFromNumberInput(numberInput) {
    const id = numberInput.id;
    const slider = document.getElementById(id.replace('angulo', 'grado').replace('vel', 'VELOCIDAD').replace('Referencia','referen').replace('POSICIONX','posx').replace('POSICIONY','posy').replace('POSICIONZ','posz'));

    // Actualizar el valor del slider cuando se cambie el cuadro de entrada
    slider.value = parseInt(numberInput.value);

    // Actualizar la variable correspondiente utilizando window[id]
    //window[id.replace('angulo', 'grado').replace('vel', 'VELOCIDAD').replace('Referencia','referen')] = parseInt(numberInput.value);
    const variableName = id.replace('angulo', 'grado').replace('vel', 'VELOCIDAD').replace('Referencia','referen').replace('POSICIONX','posx').replace('POSICIONY','posy').replace('POSICIONZ','posz');
    window[variableName] = parseInt(numberInput.value);

    // Igualar angulo1 con grado1
    for (let i = 1; i <= 7; i++) {
        if (variableName === `grado${i}`) {
            window[`angulo${i}`] = parseInt(numberInput.value);
        }
    }
    for (let i = 1; i <= 7; i++) {
        if (variableName === `VELOCIDAD${i}`) {
            window[`vel${i}`] = parseInt(numberInput.value);
        }
    }
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
        ref: parseFloat(window.Referencia),
        posx:parseFloat(window.posx),
        posy:parseFloat(window.posy),
        posz:parseFloat(window.posz),

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