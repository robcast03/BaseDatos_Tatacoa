// Función para actualizar el valor del input numérico y la variable correspondiente
function updateNumberInput(slider) {
    const id = slider.id;
    const numberInput = document.getElementById(id.replace('grado', 'angulo').replace('VELOCIDAD', 'vel').replace('referen','Referencia'));
    numberInput.value = slider.value;

    // Actualizar la variable correspondiente utilizando window[id]
    window[id.replace('grado', 'angulo').replace('VELOCIDAD', 'vel').replace('referen','Referencia')]= parseInt(slider.value);
}

// Seleccionar todos los sliders
const sliders = document.querySelectorAll('.slider');

// Agregar event listener a cada slider
sliders.forEach(slider => {
    slider.addEventListener('input', () => {
        updateNumberInput(slider);

        sendDataToPython(); // Llamar a la función para enviar los datos a Python
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
        vel1: parseFloat(window.vel1),
        vel2: parseFloat(window.vel2),
        vel3: parseFloat(window.vel3),
        vel4: parseFloat(window.vel4),
        vel5: parseFloat(window.vel5),
        vel6: parseFloat(window.vel6),
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
