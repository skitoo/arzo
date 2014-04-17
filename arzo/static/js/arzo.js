

(function($){
    $(function(){

        // get the form inputs we want to update
        var latitude = $('#latitude');
        var longitude = $('#longitude');
        var altitude = $('#altitude');
        var temp = $('#temp');

        var lat = latitude.val() !== '' ? latitude.val() : 0;
        var lon = longitude.val() !== '' ? longitude.val() : 0;
        var zoom = lat || lon ? 10 : 2;


        var ondragend = function() {
            updateLatitudeAndLongitude();
            updateAltitude();
            updateWeather();
        };

        var updateLatitudeAndLongitude = function() {
            var ll = marker.getLatLng();
            latitude.val(ll.lat);
            longitude.val(ll.lng);
        };

        var updateAltitude = function(){
            $.ajax('/api/elevation', {
                type: 'GET',
                data: {
                    latitude: latitude.val(),
                    longitude: longitude.val()
                },
                success: function(data){
                    altitude.val(parseInt(data, 10));
                }
            });
        };

        var updateWeather = function() {
            $.ajax('/api/weather', {
                type: 'GET',
                dataType: "json",
                data: {
                    latitude: latitude.val(),
                    longitude: longitude.val()
                },
                success: function(data){
                    $('#temp').html(data.temp + ' C°');
                    $('#wind_speed').html(data.wind_speed + ' km/h');
                    $('#weather-description').html(data.description);
                    $('#humidity').html(data.humidity + ' %');
                    $('#weather').removeClass();
                    $('#weather').addClass('meteocon meteocon-' + data.weather);
                }
            });
        };

        var map = L.mapbox.map('map', 'skitoo.map-2a0chld1').setView([lat, lon], zoom);

        var marker = L.marker([lat, lon], {
            draggable: true
        }).addTo(map);

        marker.on('dragend', ondragend);
        // set the initial values in the form
        updateLatitudeAndLongitude();
        updateWeather();
    });
})(jQuery);
