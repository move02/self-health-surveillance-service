//내 위치로 지도 이동
function setMyLocation(){
    let myLat = '';
    let myLng = '';
    if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(function(position){
            let myLat = position.coords.latitude;
            let myLng = position.coords.longitude;
            mainMap.setCenter(new kakao.maps.LatLng(myLat, myLng));
        });
    }
}
//map click 함수
function mapClick(mouseEvent){
    //위치 찾기
    let latlng = mouseEvent.latLng;

    //위경도 -> 주소(행정동)
    searchAddrFromCoords(latlng, 'B', function(result, status){
        if(status === kakao.maps.services.Status.OK){
            let detailAddr = '';
            let fullDetailAddr = '';
            if(!!result[0].road_address){
                detailAddr = result[0].road_address.region_1depth_name
                            + " " + result[0].road_address.region_2depth_name;
                fullDetailAddr = result[0].road_address.address_name;
            } else {
                detailAddr = result[0].address.region_1depth_name
                            + " " + result[0].address.region_2depth_name;
                fullDetailAddr = result[0].address.address_name;
            }

            //검색어 저장
            saveSearchKeyword(fullDetailAddr, 'map');

            //주소로 검색
            let searchOption = {
                location : new daum.maps.LatLng(latlng.getLat(), latlng.getLng()), // 검색 중심좌표
                radius : 5000, // 검색 범위 반경 5km
                size : 15, // 검색결과 한 페이지 출력 개수
                sort : "distance",//"accuracy", // 검색결과 정렬 옵션
                page : Number(1)
            };
            /*
            let searchOption = {
                sort : 'distance'
            };
            */
            document.getElementById('searchKeyword').value = '';

            kakaoMapSearchKeyword(fullDetailAddr, searchKeywordCallBack, searchOption);
        }
   });
}

//카카오 장소 검색 API
function kakaoMapSearchKeyword(keyword, searchCallBack, searchOptions){
    let searchList = '';

    if (!keyword.replace(/^\s+|\s+$/g, '')) {
        Swal.fire('장소 입력', '장소 키워드를 입력해주세요.', 'warning');
        return false;
    }

    /*
    //{query : keyword, sort : 'accuracy'}
    //로컬 키워드로 장소 검색 API
    //카카오 맵에서 장소검색과 같은 결과를 가져옴
    //목록표출 및 pagination생성 작업은 해야됨
    let searchData = searchOptions;
    searchData.query = keyword;
    $.ajax({
        url : 'https://dapi.kakao.com/v2/local/search/keyword.json',
        type : 'GET',
        data : searchData,
        beforeSend : function(xhr){
            xhr.setRequestHeader("Content-type", "application/json");
            xhr.setRequestHeader("Authorization", "KakaoAK daa9a8423eee246df6cf2e80e39c47d1");
        },
        success : function(result){
            console.log(result);
            let status = '';
            if(result.meta.total_count > 0){
                status = kakao.maps.services.Status.OK;
            } else if(result.meta.total_count == 0){
                status = kakao.maps.services.Status.ZERO_RESULT;
            }
            if(searchData.page){
                result.meta.nowPage = searchData.page;
            } else {
                result.meta.nowPage = 1;
            }
            searchCallBack(result.documents, status, result.meta);
        }
    });
    */

    let placeSearch = new kakao.maps.services.Places();
    if(searchOptions){
        placeSearch.keywordSearch(keyword, searchCallBack, searchOptions);
    } else {
        placeSearch.keywordSearch(keyword, searchCallBack);
    }

}

//마커를 생성하고 지도 위에 마커를 표시하는 함수입니다
//idx, mkType, title, data
function addMarker(position, options) {
    let defaultOptions = {
        idx : 0,
        mkType : '',
        title : '',
        data : null,
        tabId : '',
        zIndex : 1
    };

    options = $.extend(defaultOptions, options || {});

    let idx = options.idx;
    let mkType = options.mkType;
    let title = options.title;
    let zIndex = options.zIndex;
    let data = options.data;
    let tabId = options.tabId;

    let imageSrc = '';
    let imageSize = '';
    let imgOptions = '';
    if(mkType == 'search'){
        imageSrc = '/user/images/marker/search/pins-spot-' + (idx >= 9 ? (idx + 1) : "0"+(idx + 1)) + '.png';
        imageSize = new kakao.maps.Size(24, 37);  // 마커 이미지의 크기
        imgOptions = {offset: new kakao.maps.Point(12, 37)};
    } else {
        imageSrc = '/user/images/marker/path/mark_0'+tabId.replace('tabs','')+'.png'; // 마커 이미지 url
        imageSize = new kakao.maps.Size(29, 40);
        imgOptions = {offset: new kakao.maps.Point(14, 40)};
    }

    let markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imgOptions);

    let markerOptions = {
            position: position, // 마커의 위치
            image: markerImage,
            title: title,
            zIndex : zIndex
    };

    let markerItem = new kakao.maps.Marker(markerOptions);

    markerItem.setMap(mainMap); // 지도 위에 마커를 표출합니다

    if(mkType == 'search'){
        searchMarkers.push(markerItem);
    } else {
        //현재 활성화 되있는 탭 아이디 가져오기
        let tabId = options.tabId;
        let activeMarkersArr = markers.get(tabId);
        if(activeMarkersArr == undefined || activeMarkersArr == null){
            activeMarkersArr = [];
        }
        // 배열에 생성된 마커를 추가합니다
        activeMarkersArr.push({id : data.id, data : data, mk : markerItem});
        markers.set(tabId, activeMarkersArr);
    }

    return markerItem;
}

//지도 위에 표시되고 있는 마커를 모두 제거합니다
function removeMarker(mkType, idx, tabsId) {
    if(idx != null && idx != undefined){
        if(mkType == 'search'){
            searchMarkers[idx].setMap(null);
            searchMarkers.splice(idx, 1);
        } else {
            let markersArr = markers.get(tabsId);
            markersArr[idx].mk.setMap(null);
            markersArr.splice(idx, 1);
            markers.set(tabsId, markersArr);
        }
    } else {
        if(mkType == 'search'){
            for (let i = 0; i < searchMarkers.length; i++ ) {
                searchMarkers[i].setMap(null);
            }
        } else {
            let tabs = document.getElementById('dateTab-content').getElementsByClassName('tab-pane');
            for (let j = 0; j < tabs.length; j++){
                let tabsId = tabs[j].id;
                let tabInMarkers = markers.get(tabsId);
                if(tabInMarkers != null && tabInMarkers != undefined && tabInMarkers != ''){
                    for (let i = 0; i < tabInMarkers.length; i++) {
                        tabInMarkers[i].mk.setMap(null);
                    }
                }
            }
        }

        if(mkType == 'search'){
            searchMarkers = [];
        } else {
            markers.clear();
        }
    }
}
//마커 이미지 변경
function setMarkerImage(setMarker, imgSrc, size, offset, idx){
    imageSrc = imgSrc;
    let markerSize = size;
    let markerOffset = offset;
    let newImage = new kakao.maps.MarkerImage(imageSrc, markerSize, markerOffset);
    setMarker.setImage(newImage);
    setMarker.setZIndex(idx);
}

//좌표로 주소 정보 요청함수
function searchAddrFromCoords(coords, type, callback) {
    if(type == 'H'){
        // 좌표로 행정동 주소 정보를 요청합니다
        geocoder.coord2RegionCode(coords.getLng(), coords.getLat(), callback);
    } else {
        // 좌표로 법정동 상세 주소 정보를 요청합니다
        geocoder.coord2Address(coords.getLng(), coords.getLat(), callback);
    }
}

//선 그리기
function drawLineToMap(options){
    let defaultOptions = {
        stPoint : '',
        endPoint : '',
        color : '#000',
        weight : 1,
        opacity : 1,
        style : 'solid',
        endArrow : false,
        tabId : '',
        zIndex : 3
    };

    options = $.extend(defaultOptions, options || {});

    // 지도에 표시할 선을 생성합니다
    let polyline = new kakao.maps.Polyline({
        path: [options.stPoint, options.endPoint], // 선을 구성하는 좌표배열 입니다
        strokeWeight: options.weight, // 선의 두께 입니다
        strokeColor: options.color, // 선의 색깔입니다
        strokeOpacity: options.opacity, // 선의 불투명도 입니다 1에서 0 사이의 값이며 0에 가까울수록 투명합니다
        strokeStyle: options.style, // 선의 스타일입니다
        endArrow : options.endArrow, //끝 화살표 여부
        zIndex : options.zIndex
    });
    polyline.setMap(mainMap);

    kakao.maps.event.addListener(polyline, 'mouseover', function(mouseEvent){
        var latlng = mouseEvent.latLng;
        this.setOptions({
            strokeWeight : 5,
            strokeOpacity : 1,
            strokeStyle : 'dashed',
            zIndex : 10,
        });
    });

    kakao.maps.event.addListener(polyline, 'mouseout', function(mouseEvent){
        var latlng = mouseEvent.latLng;
        this.setOptions({
            strokeWeight : 2,
            strokeOpacity : 0.8,
            strokeStyle : 'solid',
            zIndex : 3
        });
    });

    let activeLine = userPolyline.get(options.tabId);
    if(activeLine == undefined || activeLine == null){
        activeLine = [];
    }
    activeLine.push(polyline);
    userPolyline.set(options.tabId, activeLine);
}

//라인 삭제
function removePolyLine(idx, tabsId){
    if(idx != null && idx != undefined){
        let polyLineArr = userPolyline.get(tabsId);
        if(polyLineArr.length == idx){
            idx = idx - 1;
        }
        if(polyLineArr.length != 0){
            polyLineArr[idx].setMap(null);
            polyLineArr.splice(idx, 1);
            userPolyline.set(tabsId, polyLineArr);
        }
    } else {
        let tabs = document.getElementById('dateTab-content').getElementsByClassName('tab-pane');
        for (let j = 0; j < tabs.length; j++){
            let tabsId = tabs[j].id;
            let tabInPolylines = userPolyline.get(tabsId);
            if(tabInPolylines != null && tabInPolylines != undefined && tabInPolylines != ''){
                for (let i = 0; i < tabInPolylines.length; i++) {
                    tabInPolylines[i].setMap(null);
                }
            }
        }
        userPolyline.clear();
    }
}


//오버레이 설정
function addOverlay(position, options){
    let defaultOptions = {
        content : '',
        xAnchor : '',
        yAnchor : '',
        tabId : '',
        zIndex : 2
    };

    options = $.extend(defaultOptions, options || {});

    let content = options.content;
    let xAnchor = options.xAnchor;
    let yAnchor = options.yAnchor;
    let zIndex = options.zIndex;
    let tabId = options.tabId;

    let overlayContent = '<div class="pointOverlay">'+content+'</div>';

    let customOverlayOptions = {
        position : position,
        content : overlayContent,
        zIndex : zIndex
    };

    if(xAnchor != null && xAnchor != '' && xAnchor != undefined){
        customOverlayOptions.xAnchor = xAnchor;
    }

    if(yAnchor != null && yAnchor != '' && yAnchor != undefined){
        customOverlayOptions.yAnchor = yAnchor;
    }

    let customOverlay = new kakao.maps.CustomOverlay(customOverlayOptions);

    customOverlay.setMap(mainMap);

    return customOverlay;
}

//지도 위에 표시되고 있는 마커를 모두 제거합니다
function removeOverlay(idx, tabsId) {
    if(idx != null && idx != undefined){
        let overlayArr = userOverlay.get(tabsId);
        overlayArr[idx].ol.setMap(null);
        overlayArr.splice(idx, 1);
        userOverlay.set(tabsId, overlayArr);
    } else {
        let tabs = document.getElementById('dateTab-content').getElementsByClassName('tab-pane');
        for (let j = 0; j < tabs.length; j++){
            let tabsId = tabs[j].id;
            let tabInOverlays = userOverlay.get(tabsId);
            if(tabInOverlays != null && tabInOverlays != undefined && tabInOverlays != ''){
                for (let i = 0; i < tabInOverlays.length; i++) {
                    tabInOverlays[i].ol.setMap(null);
                }
            }
        }
        userOverlay.clear();
    }
}

function getPointToMarkerList(position){
    let sw = new kakao.maps.LatLng(position.getLat() - 0.0001, position.getLng() - 0.0001);
    let ne = new kakao.maps.LatLng(position.getLat() + 0.0001, position.getLng() + 0.0001);
    let lb = new kakao.maps.LatLngBounds(sw, ne);

    let pointMarkerList = [];

    for(let i = 0; i < searchMarkers.length; i++){
        if(lb.contain(searchMarkers[i].getPosition())){
            pointMarkerList.push({idx : i, mk : searchMarkers[i]});
        }
    }

    return pointMarkerList;
}

function showHideMapObject(options){
    let defaultOptions = {
        mode : '',
        type : '',
        tabId : '',
        idx : null
    };

    options = $.extend(defaultOptions, options || {});
    let idx = options.idx;

    let mapObject = null;
    if(options.mode == 'show'){
        mapObject = mainMap;
    }

    if(options.type == 'marker'){
        let activeMarkerArr = markers.get(options.tabId);
        if(idx != null && idx != undefined && idx != ''){
            //마커 1개
            activeMarkerArr[idx].mk.setMap(mapObject);
        } else {
            //마커 전체
            if(activeMarkerArr == undefined){
                activeMarkerArr = [];
            }
            for(let i = 0; i < activeMarkerArr.length; i++){
                activeMarkerArr[i].mk.setMap(mapObject);
            }
        }
    } else if(options.type == 'overlay'){
        let activeOverlayArr = userOverlay.get(options.tabId);
        if(idx != null && idx != undefined && idx != ''){
            //오버레이 1개
            activeOverlayArr[idx].ol.setMap(mapObject);
        } else {
            //오버레이 전체
            if(activeOverlayArr == undefined){
                activeOverlayArr = [];
            }
            for(let i = 0; i < activeOverlayArr.length; i++){
                activeOverlayArr[i].ol.setMap(mapObject);
            }
        }
    } else if(options.type == 'polyline'){
        let activePolylineArr = userPolyline.get(options.tabId);
        if(idx != null && idx != undefined && idx != ''){
            //폴리라인 1개
            activePolylineArr[idx].setMap(mapObject);
        } else {
            //폴리라인 전체
            if(activePolylineArr == undefined){
                activePolylineArr = [];
            }
            for(let i = 0; i < activePolylineArr.length; i++){
                activePolylineArr[i].setMap(mapObject);
            }
        }
    } else {
        options.type = 'marker';
        showHideMapObject(options);
        options.type = 'overlay';
        showHideMapObject(options);
        options.type = 'polyline';
        showHideMapObject(options);
    }
}