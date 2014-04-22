
(function($){
    $(function(){
        var latitude = $('#observatory').data('latitude');
        var longitude = $('#observatory').data('longitude');
        var source = $("#weather-template").html();
        var template = Handlebars.compile(source);

        var updateWeather = function(){
            $.ajax('/api/weather', {
                type: 'GET',
                dataType: "json",
                data: {
                    latitude: latitude,
                    longitude: longitude
                },
                success: function(data) {
                    $("#weather-content").html(template(data));
                }
            });
        };

        var buildMap = function(){
            var map = L.mapbox.map(
                'map',
                'skitoo.map-2a0chld1',
                {
                    legendControl: {
                        position: 'topright'
                    }
                }
            ).setView([latitude, longitude], 10);
            var marker = L.marker([latitude, longitude]).addTo(map);
            map.legendControl.addLegend($('#map-legend').html());
        };

        buildMap();
        updateWeather();
        setInterval(updateWeather, 1000 * 60 * 5); // refresh every 5 minutes
    });
})(jQuery);
