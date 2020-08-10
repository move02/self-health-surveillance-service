function kakaoMapInit(){
    let mapContainer = document.getElementById('mainMap');

    //내 위치 설정
    setMyLocation();

    let options = {
        center: new kakao.maps.LatLng(36.49945333748601, 127.32882064412809), //지도의 중심좌표(산학연클러스터).
        //center: new kakao.maps.LatLng(myLat, myLng), //지도의 중심좌표(산학연클러스터).
	    level: 3 //지도의 레벨(확대, 축소 정도)
    };

    mainMap = new kakao.maps.Map(mapContainer, options);

    geocoder = new kakao.maps.services.Geocoder();

    //지도 컨트롤 추가
    zoomControl = new kakao.maps.ZoomControl();
    mainMap.addControl(zoomControl, kakao.maps.ControlPosition.RIGHT);

    kakao.maps.event.addListener(mainMap, 'click', function(mouseEvent){
        mapClick(mouseEvent);
    });
}

