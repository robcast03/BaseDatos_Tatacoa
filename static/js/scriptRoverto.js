var socket = io();

        // Definir variables globales para latitud y longitud
        var latitud = null;
        var longitud = null;
        var map = null;
        var marker = null;

        function iniciarMapa() {
            if (latitud !== null && longitud !== null) {
                var coord = { lat: latitud, lng: longitud };
                if (!map) {
                    map = new google.maps.Map(document.getElementById('map'), {
                        zoom: 15,
                        center: coord
                    });
                    marker = new google.maps.Marker({
                        position: coord,
                        map: map
                    });
                } else {
                    map.setCenter(coord);
                    marker.setPosition(coord);
                }
            }
        }

        // Asegúrate de que iniciarMapa sea accesible globalmente
        window.iniciarMapa = iniciarMapa;

        socket.on('update_values', function(data) {
            document.getElementById('direccion').innerText = data.direccion;
            document.getElementById('ruedas').innerText = data.ruedas;
            document.getElementById('temperatureValue').innerText = data.temperatura;
            document.getElementById('pressureValue').innerText = data.presion;
            document.getElementById('altitudeValue').innerText = data.altitud;
            document.getElementById('gasValue').innerText = data.gas;
            document.getElementById('distanceValue').innerText = data.distancia;
            document.getElementById('ledValue').innerText = data.led;
            document.getElementById('lat').innerText = data.lat;
            document.getElementById('lon').innerText = data.lon;

            // Asignar los valores recibidos a las variables latitud y longitud
            latitud = parseFloat(data.lat);
            longitud = parseFloat(data.lon);

            // Llamar a iniciarMapa para actualizar el mapa
            iniciarMapa();
        });

