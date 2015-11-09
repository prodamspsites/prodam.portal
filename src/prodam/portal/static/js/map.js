var map;
var geocoder;
var infoWindow;
var gMarkers = [];
var directionsDisplay;
var directionsService = new google.maps.DirectionsService();

function initialize() {
    directionsDisplay = new google.maps.DirectionsRenderer();
    var latlng = new google.maps.LatLng(-18.8800397, -47.05878999999999);

     var mapOptions = {
            center: latlng,
            zoom: 9,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
     };

     map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
     directionsDisplay.setMap(map);
     geocoder = new google.maps.Geocoder();
     infoWindow = new google.maps.InfoWindow();

     google.maps.event.addListener(map, 'click', function() {
            infoWindow.close();
     });

}
google.maps.event.addDomListener(window, 'load', initialize);

function displayPontos(){
     $.getJSON(urlJson , function(pontos){
            var bounds = new google.maps.LatLngBounds();
            $.each(pontos , function(index , ponto){
                    var latlng = new google.maps.LatLng(ponto.lat, ponto.lng);
                    var nome = ponto.nome;
                    var morada1 = ponto.morada1;
                    var morada2 = ponto.morada2;
                    var codPostal = ponto.codPostal;
                    var cat = ponto.cat;
                    if(categoriaInput == ponto.cat){
                        createMarker(latlng, nome, morada1, morada2, codPostal, cat);
                    }
                    bounds.extend(latlng);
                    map.fitBounds(bounds);
            });
     });
}
function hidePontos(){
        for(i=0; i<gMarkers.length; i++){
            if (gMarkers[i].cat == categoriaInput){
                gMarkers[i].setMap(null);
            }
        }

}

function createMarker(latlng, nome, morada1, morada2, codPostal, cat){

     var marker = new google.maps.Marker({
            map: map,
            position: latlng,
            title: nome,
            cat : cat
     });

     gMarkers.push(marker);

     google.maps.event.addListener(marker, 'click', function() {


            var iwContent = '<div id="iw_container">' +
                        '<div class="iw_title">' + nome + '</div>' +
                 '<div class="iw_content">' + morada1 + '<br />' +
                 morada2 + '<br />' +
         cat + '<br />' +
                 codPostal + '</div></div>';


            infoWindow.setContent(iwContent);
            infoWindow.open(map, marker);
     });
}
$(document).ready(function(){
    $('.menuItens > ul > li a').click(function(){
        $(this).parent().find('.subItens').toggle();
        $(this).parent().toggleClass('active');
    });
    $('ul#casa li input').click(function() {
                categoriaInput = $(this).attr('class');
        if ($(this).is(':checked')) {
                        urlJson = 'js/casa.json';
            displayPontos();
                }
        });
    $('ul#rua li input').click(function(){
        categoriaInput = $(this).attr('class');
        if ($(this).is(':checked')) {
                        urlJson = 'js/rua.json';
            displayPontos();
                }
    });
    $('ul.subItens li input').click(function(){
        categoriaInput = $(this).attr('class');
        if (!$(this).is(':checked')) {
                        hidePontos();
                }
    });
    $("form").submit(function(event) {
         event.preventDefault();
         var enderecoPartida = $("#txtEnderecoPartida").val();
         var enderecoChegada = $("#txtEnderecoChegada").val();
         var request = {
                origin: enderecoPartida,
                destination: enderecoChegada,
                travelMode: google.maps.TravelMode.DRIVING
         };
         directionsService.route(request, function(result, status) {
                    if (status == google.maps.DirectionsStatus.OK) {
                        directionsDisplay.setDirections(result);
                    }
            });
    })

    $(".txtEndereco").autocomplete({
                source: function (request, response) {
                        geocoder.geocode({ 'address': request.term + ', Brasil', 'region': 'BR' }, function (results, status) {
                                response($.map(results, function (item) {
                                        return {
                                                label: item.formatted_address,
                                                value: item.formatted_address,
                                                latitude: item.geometry.location.lat(),
                                                longitude: item.geometry.location.lng()
                                        }
                                }));
                        })
                },
        });
});