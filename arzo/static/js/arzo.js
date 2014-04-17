

(function($){
    $(function(){

        // get the form inputs we want to update
        var latitude = $('#latitude');
        var longitude = $('#longitude');

        var lat = latitude.val() !== '' ? latitude.val() : 0;
        var lon = longitude.val() !== '' ? longitude.val() : 0;
        var zoom = lat || lon ? 10 : 2;


        var ondragend = function() {
            var ll = marker.getLatLng();
            latitude.val(ll.lat);
            longitude.val(ll.lng);
        };

        var map = L.mapbox.map('map', 'skitoo.map-2a0chld1').setView([lat, lon], zoom);

        var marker = L.marker([lat, lon], {
            draggable: true
        }).addTo(map);

        marker.on('dragend', ondragend);
        // set the initial values in the form
        ondragend();
    });
})(jQuery);
