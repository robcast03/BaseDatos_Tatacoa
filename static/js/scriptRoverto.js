function iniciarMapa(){
    var coord={lat:4.683502,lng:-74.0424858};
    var map=new google.maps.Map(document.getElementById('map'),{
        zoom:15,
        center:coord
    });
    var marker = new google.maps.Marker({
        position: coord,
        map:map
    })
}
    // Tu código JavaScript aquí
    // Import the functions you need from the SDKs you need
    import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.0/firebase-app.js";
 
  // TODO: Add SDKs for Firebase products that you want to use
  // https://firebase.google.com/docs/web/setup#available-libraries

  // Your web app's Firebase configuration
  // For Firebase JS SDK v7.20.0 and later, measurementId is optional
  const firebaseConfig = {
    apiKey: "AIzaSyBkvXuvU1oCcrKKlUBsR_cCmYw8SHeKhxs",
    authDomain: "rover-resilience.firebaseapp.com",
    databaseURL: "https://rover-resilience-default-rtdb.firebaseio.com",
    projectId: "rover-resilience",
    storageBucket: "rover-resilience.appspot.com",
    messagingSenderId: "737977492853",
    appId: "1:737977492853:web:ade421db035a08a6ccdf3c",
    measurementId: "G-9HR8B1VR9W"
  };

  // Initialize Firebase
  const app = initializeApp(firebaseConfig);

    import{getDatabase, ref, child, get} from "https://www.gstatic.com/firebasejs/10.11.0/firebase-database.js";
document.addEventListener('DOMContentLoaded', function() {


const db = getDatabase();

let Temp = document.getElementById("temperatureValue");
let Pres = document.getElementById("pressureValue");
let Gas = document.getElementById("signalQuality");
let Hum = document.getElementById("humidityValue");
let Dis = document.getElementById("inclinacionValue");
let Cor2 = document.getElementById("positionValue");
let Cor3 = document.getElementById("joint5");

function RetData(){
    const dbRef = ref(db);
    get(child(dbRef, 'sensorica/')).then((snapshot)=>{

        if(snapshot.exists()){
            Temp.textContent = + snapshot.val().esp.ecAumLJGtIXxnOELuVUFRkVWQGk1.temperatura;
            Pres.textContent = + snapshot.val().esp.ecAumLJGtIXxnOELuVUFRkVWQGk1.precion;
            Gas.textContent = + snapshot.val().esp.ecAumLJGtIXxnOELuVUFRkVWQGk1.gas;
            Hum.textContent = + snapshot.val().esp.ecAumLJGtIXxnOELuVUFRkVWQGk1.hum;
            Dis.textContent = + snapshot.val().esp.ecAumLJGtIXxnOELuVUFRkVWQGk1.distancia;
            Cor2.textContent = + snapshot.val().raspi.corriente2;
            Cor3.textContent = + snapshot.val().raspi.corriente3;
        }else{
            console.log("Q paso???")
        }
    })
}
setInterval(RetData, 10);
});

// Función para actualizar los valores de los sensores en el contenedor cont_gemelo
// Suponiendo que obtienes los valores de los sensores y los actualizass en JavaScript.

