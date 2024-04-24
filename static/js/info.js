function mostrarInfo(elemento) {
    elemento.querySelector('.info').style.display = 'block';
}

function ocultarInfo(elemento) {
    elemento.querySelector('.info').style.display = 'none';
}
// tuarchivo.js

document.getElementById('botonPlanos').addEventListener('click', function() {
    // Redirige a 'brazo.html' ubicado en la carpeta 'templates'
    window.location.href = 'http://127.0.0.7:5000';
});

document.getElementById('botonModelos').addEventListener('click', function() {
    // Redirige a 'Roverto.html' ubicado en la carpeta 'templates'
    window.location.href = 'http://127.0.0.9:5000';
});

document.getElementById('botonCalculos').addEventListener('click', function() {
    // Redirige a 'joy.html' ubicado en la carpeta 'templates'
    window.location.href = 'http://127.0.0.1:5000';
});

document.getElementById('botonJoyBrazo').addEventListener('click', function() {
    // Redirige a 'joy.html' ubicado en la carpeta 'templates'
    window.location.href = 'http://127.0.0.8:5000';
});