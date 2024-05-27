
function actualizarVelocidades() {
    // Generar valores aleatorios para las velocidades de los motores (entre 0 y 100)
    let velocidades = [Motor1,Motor2,Motor3,Motor4,Motor5];
    

    // Actualizar los cuadros de velocidad con los nuevos valores
    for (let i = 0; i < 6; i++) {
        updateSpeedometer('motor' + (i + 1), velocidades[i]);
    }
}

function updateSpeedometer(id, speed) {
    var progressBar = document.getElementById(id).querySelector('.speedometer__progress');
    var speedText = document.getElementById(id).querySelector('.speedometer__text');

    // Convertir la velocidad a un porcentaje para el ancho de la barra de progreso
    var widthPercentage = (speed / 100) * 100;

    // Aplicar el ancho de la barra de progreso con transición
    progressBar.style.transition = "width 0.5s";
    progressBar.style.width = widthPercentage + "%";

    // Mostrar el valor de la velocidad
    speedText.textContent = speed + " km/h";
}


// Llamar a la función para actualizar las velocidades cada cierto intervalo de tiempo (por ejemplo, cada segundo)
setInterval(actualizarVelocidades, 1000);


// Función para actualizar el medidor de ángulo
function updateAngleMeter(angleId, newData) {
    var angleMeter = document.getElementById(angleId);
    var progress = angleMeter.querySelector('.angle-meter__progress');

    // Obtener el texto actual del ángulo
    var currentText = angleMeter.querySelector('.angle-meter__text').textContent;
    // Extraer el valor numérico actual del texto
    var currentAngle = parseFloat(currentText);

    // Establecer la opacidad máxima para mostrar el nuevo dato
    progress.style.opacity = 1;

    // Actualizar el texto del ángulo
    angleMeter.querySelector('.angle-meter__text').textContent = newData + '°';

     // Establecer el color del progreso según el nuevo dato
     if (newData > 80) {
        progress.style.backgroundColor = '#9dc1f9'; // Azul
    } else if (newData > 60) {
        progress.style.backgroundColor = '#94baf7'; // Azul más oscuro
    } else if (newData > 40) {
        progress.style.backgroundColor = '#6fd08c'; // Verde
    } else if (newData > 20) {
        progress.style.backgroundColor = '#87e7a4d7'; // Verde claro
    } else {
        progress.style.backgroundColor = '#a4a0e5bd'; // Lila mas oscuro
    }

    
    // Esperar un breve período de tiempo antes de disminuir la transparencia
    setTimeout(function() {
        // Disminuir la opacidad para volver al estado original
        progress.style.opacity = 0;
    }, 1000); // Tiempo de espera en milisegundos (ejemplo: 1000 = 1 segundo)
}

//
// Función para generar un nuevo dato aleatorio entre 0 y 100 para cada ángulo
function generateRandomData() {
    return {
        joint1: Math.floor(Math.random() * 101), // Ángulo 1
        joint2: Math.floor(Math.random() * 101), // Ángulo 2
        joint3: Math.floor(Math.random() * 101), // Ángulo 3
        joint4: Math.floor(Math.random() * 101), // Ángulo 4
        joint5: Math.floor(Math.random() * 101), // Ángulo 5
        joint6: Math.floor(Math.random() * 101)  // Ángulo 6
    };
}

// Función para actualizar los medidores de ángulo con nuevos datos aleatorios
function updateAngleMeters(data) {
    // Actualizar cada medidor de ángulo con los nuevos datos
    updateAngleMeter('joint1', Joint1);
    updateAngleMeter('joint2', Joint2);
    updateAngleMeter('joint3', Joint3);
    updateAngleMeter('joint4', Joint4);
    updateAngleMeter('joint5', Joint5);
    updateAngleMeter('joint6', data.joint6);
}

// Función para actualizar periódicamente los medidores de ángulo
function updateAnglesPeriodically() {
    // Generar nuevos datos aleatorios
    var randomData = generateRandomData();

    // Actualizar los medidores de ángulo con los nuevos datos
    updateAngleMeters(randomData);

    // Llamar recursivamente a esta función después de 2 segundos
    setTimeout(updateAnglesPeriodically, 2000);
}

// Iniciar la actualización periódica de los medidores de ángulo
updateAnglesPeriodically();

// Función para actualizar el estado de advertencia del indicador
function updateWarningIndicator(indicatorId, newData) {
    var indicator = document.getElementById(indicatorId);

    // Remover todas las clases de color
    indicator.classList.remove('red', 'yellow');

    // Agregar la clase de color correspondiente según el nuevo dato
    if (newData > 80) {
        indicator.classList.add('red'); // Rojo
    } else if (newData > 60) {
        indicator.classList.add('yellow'); // Amarillo
    }
    // Agrega más condiciones según sea necesario
}

// Llamar a la función para cada ángulo con los nuevos datos
updateWarningIndicator('warning-indicator-joint1', newDataJoint1);

