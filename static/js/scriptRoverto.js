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
// Ensure iniciarMapa is globally accessible
window.iniciarMapa = iniciarMapa;
