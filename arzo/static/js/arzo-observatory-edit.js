
(function($){
    $(function(){
        console.debug('loaded!');
        var latitude = $('#latitude');
        var longitude = $('#longitude');
        var zoom = latitude.val() && longitude.val() ? 2 : 10;

        var map = L.mapbox.map(
            'map',
            'skitoo.map-2a0chld1'
        ).setView([latitude.val(), longitude.val()], zoom);
        var marker = L.marker([latitude.val(), longitude.val()], {
            draggable: true
        }).addTo(map);

        var onChangePositionFromInputs = function() {
            marker.setLatLng(L.latLng(latitude.val(), longitude.val()));
        };

        var onDragendMarker = function() {
            var ll = marker.getLatLng();
            latitude.val(ll.lat);
            longitude.val(ll.lng);
        };

        // listeners
        $('#latitude').keyup(onChangePositionFromInputs);
        $('#longitude').keyup(onChangePositionFromInputs);
        marker.on('dragend', onDragendMarker);

    });
})(jQuery);
