// Note: This example requires that you consent to location sharing when
      // prompted by your browser. If you see the error "The Geolocation service
      // failed.", it means you probably did not give permission for the browser to
  // locate you.
    var map, infoWindow, source, dest,directionsDisplay;
      function initMap() {
        map = new google.maps.Map(document.getElementById('map'), {
          center: {lat: 36.778259, lng:  -119.417931},
          zoom: 6
        });
        infoWindow = new google.maps.InfoWindow;
        // Try HTML5 geolocation.
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };
            source = pos;
            map.setCenter(pos);
            console.log("now position is: "+ pos.lat + pos.lng);
            var marker = new google.maps.Marker({
              map:map,
              position: pos
            });
            google.maps.event.addListener(marker, 'click', function() {
              infoWindow.setContent('<div><strong>' + pos.name + '</strong><br>' + 'You are here!' + '</div>');
              infoWindow.open(map, this);
            });
            nearByPlaces(pos);
          }, function() {
            handleLocationError(true, infoWindow, map.getCenter());
          });
        } else {
          // Browser doesn't support Geolocation
          handleLocationError(false, infoWindow, map.getCenter());
        }
      }
      function handleLocationError(browserHasGeolocation, infoWindow, pos) {
        infoWindow.setPosition(pos);
        infoWindow.setContent(browserHasGeolocation ?
                              'Error: The Geolocation service failed.' :
                              'Error: Your browser doesn\'t support geolocation.');
        infoWindow.open(map);
      }
      function nearByPlaces(position) {
        var pos = {lat: position.lat, lng: position.lng}
      //  console.log("the position in near by places is:"+pos.lat + " " + pos.lng);
        map = new google.maps.Map(document.getElementById('map'), {
          center: pos,
          zoom: 16
        });
        infowindow = new google.maps.InfoWindow();
        var service = new google.maps.places.PlacesService(map);
        service.nearbySearch({
          location: pos,
          radius: 500,
          types: ['cafe'|'store'|'school'| 'restaurant']
        },callback);
      }
      function callback(results, status, pagination) {
        if (status !== google.maps.places.PlacesServiceStatus.OK) {
            return;
        } else {
          for (var i =0; i< (results.length); i++) {
            createMarker(results[i]);
          }
          if (pagination.hasNextPage) {
            pagination.nextPage();
          }
        }
      }
      function createMarker(place) {
    //    console.log("createMarker details:",place);
        var placeLoc = place.geometry.location;
        var directionsService = new google.maps.DirectionsService;
        directionsDisplay = new google.maps.DirectionsRenderer;
        directionsDisplay.setMap(null);
        if (place.types.indexOf('library') != -1) {
          var marker = new google.maps.Marker({
            map: map,
            animation: google.maps.Animation.DROP,
            title: place.name,
            icon: 'library.png',
            position: place.geometry.location
          });
        }  else if (place.types.indexOf('restaurant') != -1) {
          var marker = new google.maps.Marker({
            map: map,
            animation: google.maps.Animation.DROP,
            title: place.name,
            icon: 'rest_mini.png',
            position: place.geometry.location
          });
        } else if (place.types.indexOf('cafe') != -1) {
          var marker = new google.maps.Marker({
            map: map,
            animation: google.maps.Animation.DROP,
            title: place.name,
            icon: 'cafe_mini.png',
            position: place.geometry.location
          });
        } else {
          var marker = new google.maps.Marker({
            map: map,
            animation: google.maps.Animation.DROP,
            title: place.name,
            position: place.geometry.location
          });
        }
          var onChangeHandler = function() {
            calculateAndDisplayRoute(directionsService, directionsDisplay);
          };
        google.maps.event.addListener(marker, 'click', function() {
        //  console.log(place);
          dest = {lat:place.geometry.location.lat(), lng: place.geometry.location.lng()};
        infowindow.setContent('<div><strong>' + place.name + '</strong><br>' +
        place.vicinity + '</div>');
          infowindow.open(map, this);
          onChangeHandler();
        });
      }
      function calculateAndDisplayRoute(directionsService, directionsDisplay) {
        // console.log("calculateAndDisplayRoute being called - source:",source, "destination:", dest);
        directionsService.route({
          origin: source,
          destination: dest,
          travelMode: 'WALKING'
        }, function(response, status) {
          if (status === 'OK') {
            // console.log("status is OK:", status);
            // console.log(response);
              directionsDisplay.setMap(map);
              directionsDisplay.setDirections(response);
          } else {
            window.alert('Directions request failed due to ' + status);
          }
        });
      }
