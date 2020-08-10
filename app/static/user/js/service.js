$(document).ready(function(){
    $('#dateTab-content').on('click', '.distance_result p.pagi > .btn_close', function(){
        //마커 및 라인 삭제
        let itemIdx = $(this).parents('.item_02').index();
        let activeTabId = getActiveTabElement().id;

        removeMarker('userPickList', itemIdx, activeTabId);
        removeOverlay(itemIdx, activeTabId);
        removePolyLine(itemIdx, activeTabId);
        //element 삭제
        $(this).parents('.item_02').remove();
        changePickPlaceToNumbering();
        changePickPlaceNumberToMarkers();
        changePickPlaceNumberToDrawLine();
    });

    $('#dateTab-content').on('click', '.distance_result p.pagi > .btn_up', function(){
        let thisItem = $(this).parents('.item_02');
        let thisMarkerInfo = thisItem.data('placeId');
        let prevItem = thisItem.prev();
        if(prevItem[0]){
            prevItem.before(thisItem);
        }
        changePickPlaceToNumbering();
        changePickPlaceNumberToMarkers();
        changePickPlaceNumberToDrawLine();
    });

    $('#dateTab-content').on('click', '.distance_result p.pagi > .btn_down', function(){
        let thisItem = $(this).parents('.item_02');
        let thisMarkerInfo = thisItem.data('placeId');
        let nextItem = thisItem.next();
        if(nextItem[0]){
            nextItem.after(thisItem);
        }
        changePickPlaceToNumbering();
        changePickPlaceNumberToMarkers();
        changePickPlaceNumberToDrawLine();
    });

    $('.pick_wrap_footer').on('click', '.analysisSt', function(){
        //날짜 확인
        let baseDate = $('#baseDate').val();
        let baseDateReg = /^(19|20)\d{2}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[0-1])$/;
        if(!baseDateReg.test(baseDate)){
            Swal.fire('기준날짜입력', '기준날짜를 입력해주세요.', 'warning');
            return ;
        }

        $('#analysisStModal').modal();
    });

    //tab 추가
    $('#addTabs').click(function(){
        let tabCnt = $('#dateTabs > li').length;

        if(tabCnt > 5){
            Swal.fire('알림', '경로 추가 일차는 최대 5일차까지 입니다.', 'warning');
            return ;
        }

        let newTabNav = '<li class="nav-item">';
        newTabNav += '<a class="nav-link" data-toggle="pill" href="#tabs'+tabCnt+'">'+tabCnt+'일차</a>';
        newTabNav += '</li>';

        $('#dateTabs > li').last().before(newTabNav);

        let newTabContent = '<div id="tabs'+tabCnt+'" class="container tab-pane">';
        newTabContent += '<div class="distance_result"><ul></ul></div></div>';

        $('#dateTab-content').append(newTabContent);
    });

    $('#dateTabs').on('click', 'li.nav-item', function(){
        if($(this).hasClass('addTabLi')){
            return;
        }
        //현재 활성화 되는 tab에 맞게 지도에 마커 및 라인 그리기
        let prevTabId = getActiveTabElement().id;
        showHideMapObject({mode:'hide', type:'all', tabId:prevTabId});

        let activeTabId = $(this).find('a.nav-link').attr('href').replace('#','');
        showHideMapObject({mode:'show', type:'all', tabId:activeTabId});

        let activeMarkers = markers.get(activeTabId);
        if(activeMarkers != undefined && activeMarkers != null){
            let newbounds = new kakao.maps.LatLngBounds();
            for(let i = 0; i < activeMarkers.length; i++){
                newbounds.extend(activeMarkers[i].mk.getPosition());
            }
            mainMap.setBounds(newbounds);
        }
    });

    $('#analysisStModal').on('click', '#infoSave', function(){
        let parentModalEl = $(this).parents('#analysisStModal');
        //동의 여부 체크 해야됨
        if($('input[name="agree"]:checked').val() == 'N'){
            Swal.fire('공유동의확인', '경로 정보 동의를 체크해주세요.', 'warning');
            return ;
        }

        if(parentModalEl.find('#reside_area').val() == ''){
            Swal.fire('거주지역확인', '거주지역을 선택해주세요.', 'warning');
            return ;
        }

        if(parentModalEl.find('#telno').val() == ''){
            Swal.fire('연락처확인', '연락처을 입력해주세요.', 'warning');
            return ;
        }

        if(parentModalEl.find('#password').val() != parentModalEl.find('#passConfirm').val()){
            Swal.fire('비밀번호확인', '비밀번호를 확인해주세요.', 'warning');
            return ;
        }

        let userInfoData = setUserInfoData();

        $.ajax({
            url : '/analysis/userInfo/save',
            type : 'POST',
            contentType : 'application/json',
            dataType : 'json',
            data : JSON.stringify(userInfoData),
            success : function(result){
                console.log(result);
                if(result.responseText == 'success'){
                    $('#analysisStModal').modal('hide');
                    let resultHtml = makeResultHtml(result);
                    Swal.fire({
                        title: '<strong>분석결과</strong>',
                        icon: 'info',
                        html: resultHtml,
                        showCloseButton: true,
                        showCancelButton: true,
                        focusConfirm: false,
                        confirmButtonText: 'OK',
                        confirmButtonAriaLabel: 'OK',
                    });
                }
            }, error : function(result){
                console.log(result);
            }
        });
    });

    $('#analysisStModal').on('click', '#infoNonSave', function(){
        let userInfoData = setUserInfoData();

        $.ajax({
            url : '/analysis/userInfo',
            type : 'POST',
            contentType : 'application/json',
            dataType : 'json',
            data : JSON.stringify(userInfoData),
            success : function(result){
                console.log(result);
            }, error : function(result){
                console.log(result);
            }
        });
    });
})

function saveSearchKeyword(keyword, type){
    insertData = {};
    insertData.keyword = keyword;
    insertData.searchType = type;
    $.ajax({
        url : '/keyword/save',
        type : 'POST',
        contentType : 'application/json',
        dataType : 'json',
        data : JSON.stringify(insertData),
        success : function(result){
            console.log(result);
        }, error : function(result){
            console.log(result);
        }
    });
}

function savePickPlace(placeInfo){
    insertData = {};
    insertData.place_id = placeInfo.id;
    insertData.place_name = placeInfo.place_name;
    insertData.place_address = placeInfo.address_name;
    insertData.place_road_address = placeInfo.road_address_name;
    insertData.lat = placeInfo.y;
    insertData.lng = placeInfo.x;
    insertData.place_ctprvn = placeInfo.address_name.replace();
    insertData.place_signgu = placeInfo.address_name.replace();
    $.ajax({
        url : '/pickPlace/save',
        type : 'POST',
        contentType : 'application/json',
        dataType : 'json',
        data : JSON.stringify(insertData),
        success : function(result){
            console.log(result);
        }, error : function(result){
            console.log(result);
        }
    });
}

function setUserInfoData(){
    //사용자 정보
    let userInfoData = $('#userInfoMForm').serializeObject();

    //경로 데이터 넣기
    let pickPlaceTabListEl = document.getElementById('dateTab-content').getElementsByClassName('tab-pane');

    let baseDate = document.getElementById('baseDate').value;
    let userLocation = [];
    for(let i = 0; i < pickPlaceTabListEl.length; i++){
        let pickPlaceListEl = pickPlaceTabListEl[i].getElementsByClassName('item_02');

        let coursDate = getDate(baseDate, 'plus', 'day', (i+1));
        for(let j = 0; j < pickPlaceListEl.length; j++){

            let itemDataEl = $(pickPlaceListEl[j]);
            let markerInfo = itemDataEl.data('marker-info');
            let placeInfo = itemDataEl.data('place-info');
            let locationData = {};
            locationData.deOrdr = i+1;
            locationData.visitTime = pickPlaceListEl[j].getElementsByClassName('time_01')[0].value;
            locationData.coursDate = coursDate.format('yyyy-MM-dd');
            locationData.lat = markerInfo.getPosition().getLat();
            locationData.lng = markerInfo.getPosition().getLng();
            locationData.place_id = placeInfo.id;
            locationData.place_name = placeInfo.place_name;
            locationData.place_address = placeInfo.address_name;
            locationData.place_road_address = placeInfo.road_address_name;

            userLocation.push(locationData);
        }
    }
    userInfoData.location = userLocation;

    return userInfoData;
}

function makeResultHtml(resultData){
    let htmlStr = '<p>결과는!!!!</p>';

    return htmlStr;
}

function fnSearchKeydown(obj, event) {
	if(event.keyCode == 13){
        $(obj).blur();
        setTimeout(function(e) {
            $("#srchKeywordBttn").click();
        },200);
	}
	return false;
}

function srchSubmit(){

    let searchKeyword = document.getElementById('searchKeyword').value;

    //검색어 저장
    saveSearchKeyword(searchKeyword, 'search');

    //현재 지도 중심좌표로 검색
    let mapCenterLatLng = mainMap.getCenter();

    searchOption = {
        //location : new daum.maps.LatLng(mapCenterLatLng.getLat(), mapCenterLatLng.getLng()), // 검색 중심좌표
        radius : 15000, // 검색 범위 반경 15km
        size : 15, // 검색결과 한 페이지 출력 개수
        sort : "accuracy", // 검색결과 정렬 옵션
        page : Number(1)
    };
    /*
    let searchOption = {
        sort : 'accuracy'
    };
    */
    //카카오 장소 검색 API
    kakaoMapSearchKeyword(searchKeyword, searchKeywordCallBack, searchOption);
}

// Daum 검색 api 조회 후 목록 만들기
function searchKeywordCallBack(data, status, pagination){
//function searchKeywordCallBack(data, status, meta){
    if(status === kakao.maps.services.Status.OK){

        if(mobilePlaceOverlay != '') {
            mobilePlaceOverlay.remove();
        }
        let listEl = document.getElementById('search-list');
        let bounds = new kakao.maps.LatLngBounds();
        // 정상적으로 검색이 완료됐으면 검색 목록과 마커를 표출.
        //검색 목록 삭제
        removeAllChildNodes(listEl);
        //지도의 검색 마커 삭제
        removeMarker('search');
        //검색 마커 및 목록 추가
        for(let i = 0; i < data.length; i++){
            let placePosition = new kakao.maps.LatLng(data[i].y, data[i].x);
            let placeMarker = addMarker(placePosition, {idx:i, mkType:'search', title:data[i].place_name});

            //목록 생성
            let itemEl = getSearchListItem(i, data[i]);

            //지도 범위 재설정을 위한 마커 위치 추가
            bounds.extend(placePosition);

            //마커 및 목록 마우스오버 시 인포윈도우 표시
            (function(marker, placeInfo, idx){
                kakao.maps.event.addListener(marker, 'mouseover', function(){
                    imageSrc = '/user/images/marker/search/pins-spot-' + (idx >= 9 ? (idx + 1) : "0"+(idx + 1)) + '-over.png';
                    setMarkerImage(marker, imageSrc, new kakao.maps.Size(24, 37), new kakao.maps.Point(12, 37), 5);
                    mkPlaceOverlay = addOverlay(marker.getPosition(), {content:placeInfo.place_name, xAnchor:0.5, yAnchor:0.5});
                });

                kakao.maps.event.addListener(marker, 'mouseout', function(){
                    imageSrc = '/user/images/marker/search/pins-spot-' + (idx >= 9 ? (idx + 1) : "0"+(idx + 1)) + '.png';
                    setMarkerImage(marker, imageSrc, new kakao.maps.Size(24, 37), new kakao.maps.Point(12, 37), 1);
                    mkPlaceOverlay.setMap(null);
                });
                kakao.maps.event.addListener(marker, 'click',  function(){
                    if(isMobile()){
                        if(mobilePlaceOverlay != '') {
                            mobilePlaceOverlay.remove();
                        }
                        if(mkPlaceOverlay != ''){
                            mkPlaceOverlay.setMap(null);
                        }
                        let pointMarkers = getPointToMarkerList(marker.getPosition());
                        if(pointMarkers.length == 1){
                            mkPlaceOverlay = addOverlay(pointMarkers[0].mk.getPosition(), {content:pointMarkers[0].mk.getTitle(), xAnchor:0.5, yAnchor:0.5});
                        } else if(pointMarkers.length > 1){
                            let contentList = '';
                            let mobileOverlayEl = document.createElement('div');
                            mobileOverlayEl.classList.add('mobileOverlay');
                            mobileOverlayEl.style.top = '0px';
                            mobileOverlayEl.style.left = '0px';
                            contentList += '<ul>';
                            for(let i = 0; i < pointMarkers.length; i++){
                                let idx = pointMarkers[i].idx;

                                contentList += '<li>';
                                contentList += '<a href="javascript:fn_m_clickSearchResultList('+idx+');">';
                                contentList += '<span class="m_search_icon">';
                                contentList += '<img src="/user/images/marker/search/pins-spot-'+(idx >= 9 ? (idx+1) : "0"+(idx +1))+'.png" width="20" align="middle">';
                                contentList += '</span>';
                                contentList += pointMarkers[i].mk.getTitle();
                                contentList += '</a>';
                                contentList += '</li>';
                            }
                            contentList += '</ul>';
                            mobileOverlayEl.innerHTML = contentList;

                            document.getElementById('mainMap').appendChild(mobileOverlayEl);

                            mobilePlaceOverlay = mobileOverlayEl;
                        }
                    }
                });
                itemEl.onmouseover = function(){
                    imageSrc = '/user/images/marker/search/pins-spot-' + (idx >= 9 ? (idx + 1) : "0"+(idx + 1)) + '-over.png';
                    setMarkerImage(marker, imageSrc, new kakao.maps.Size(24, 37), new kakao.maps.Point(12, 37), 5);
                    mkPlaceOverlay = addOverlay(marker.getPosition(), {content:placeInfo.place_name, xAnchor:0.5, yAnchor:0.5});
                };
                itemEl.onmouseout = function(){
                    imageSrc = '/user/images/marker/search/pins-spot-' + (idx >= 9 ? (idx + 1) : "0"+(idx + 1)) + '.png';
                    setMarkerImage(marker, imageSrc, new kakao.maps.Size(24, 37), new kakao.maps.Point(12, 37), 1);
                    mkPlaceOverlay.setMap(null);
                };
                itemEl.onclick = function(){
                    //레이어 보이기
                    if($('#pick_wrap').css('display') == 'none'){
                        $('#pick_wrap').show();
                    }
                    //현재 활성화된 tab
                    let activeTab = getActiveTabElement();

                    let latlng = marker.getPosition();
                    //마커 추가
                    let newMarker = addMarker(latlng, {mkType:'userPoint', title:placeInfo.place_name, data:placeInfo, tabId:activeTab.id});
                    //오버레이 추가
                    let newMkPlaceOverlay = addOverlay(newMarker.getPosition(), {content:placeInfo.place_name, xAnchor:0.5, yAnchor:0.5});
                    let activeUserOverlayArr = userOverlay.get(activeTab.id);
                    if(activeUserOverlayArr == undefined || activeUserOverlayArr == null){
                        activeUserOverlayArr = [];
                    }
                    activeUserOverlayArr.push({id : placeInfo.id, ol : newMkPlaceOverlay});
                    userOverlay.set(activeTab.id, activeUserOverlayArr);

                    //이전 마커에서 현재 마커까지 라인 그리기
                    let activeMarkers = markers.get(activeTab.id);
                    if(activeMarkers.length > 1){
                        drawOptions = {
                            stPoint : activeMarkers[activeMarkers.length - 2].mk.getPosition(),
                            endPoint : new kakao.maps.LatLng(latlng.getLat(), latlng.getLng()),
                            weight : 2,
                            color : '#dc3545',
                            opacity : 0.8,
                            style : 'solid',
                            endArrow : true,
                            tabId : activeTab.id
                        };
                        drawLineToMap(drawOptions);
                    }
                    let newItemEl = addUserPickPlaceItemEl(placeInfo);

                    //element에 장소와 마커 정보 넣기
                    $(newItemEl).data('marker-info', newMarker);
                    $(newItemEl).data('place-id', placeInfo.id);
                    $(newItemEl).data('place-info', placeInfo);

                    let newbounds = new kakao.maps.LatLngBounds();
                    for(let i = 0; i < activeMarkers.length; i++){
                        newbounds.extend(activeMarkers[i].mk.getPosition());
                    }
                    mainMap.setBounds(newbounds);

                    //선택한 정보 DB에 저장
                    savePickPlace(placeInfo);

                }
            })(placeMarker, data[i], i);

            listEl.appendChild(itemEl);
        }

        //검색된 목록들이 모두 보이게 지도 범위 재설정
        mainMap.setBounds(bounds);

        //검색 결과 건수 표시
        document.getElementsByClassName('result_num')[0].innerHTML = '검색결과 : '+pagination.totalCount+'건';

        // 페이지 번호를 표출합니다
        let paginationEl = getPagination(pagination);
        //let paginationEl = getPaginationMeta(meta);
        listEl.appendChild(paginationEl);
    } else if(status === kakao.maps.services.Status.ZERO_RESULT){
        Swal.fire('장소 입력', '검색 결과가 존재하지 않습니다.', 'warning');
        return;
    } else {
        Swal.fire('장소 입력', '검색 결과 중 오류가 발생했습니다.', 'warning');
        return;
    }
}



function fn_m_clickSearchResultList(idx){
    let listEl = document.getElementById('search-list').getElementsByTagName('li');
    if(idx != null && idx != undefined){
        listEl[idx].click();
    }
}

function getSearchListItem(index, places){
    let el = document.createElement('li');

    el.classList.add('item');

    itemStr = '<span class="marker">'+(index+1)+'</span>';
    itemStr += '<div class="info">';
    itemStr += '<h5>'+places.place_name+'</h5>';
    itemStr += '<span class="place">'+places.category_group_name+'</span>';
    if (places.road_address_name) {
        itemStr += '<span class="address">' + places.road_address_name + '</span>';
    } else {
        itemStr += '<span class="address">' +  places.address_name  + '</span>';
    }
    itemStr += '<span class="tel">'+places.phone+'</span>';
    itemStr += '</div>';

    el.innerHTML = itemStr;

    return el;
}
/*
//검색결과 목록 하단에 페이지번호를 표시는 함수입니다
//REST API meta로 생성
function getPaginationMeta(meta){
    let paginationEl = document.createElement('div');
    paginationEl.classList.add('list-group-item');
    paginationEl.classList.add('list-group-item-action');
    paginationEl.classList.add('bg-light');
    paginationEl.classList.add('search-pagination');

    //전체 페이지
    //page = 6
    // => < 5 6 7 8 >
    // 125, totalPage : 9,
    let listCount = 15;
    let pageCount = 4;
    let page = meta.nowPage;
    let totalCount = meta.total_count;
    let totalPage = Math.ceil((totalCount-1) / listCount) + 1;
    if(totalCount % listCount > 0){
        totalPage++;
    }
    if(totalPage < page){
        page = totalPage;
    }

    let startPage = (Math.floor((page - 1) / pageCount)) * pageCount + 1;
    let endPage = startPage + pageCount - 1;

    if(endPage > totalPage){
        endPage = totalPage;
    }

    let prevPage = startPage-1;
    let nextPage = startPage+1;

    if(page > 1){
        paginationEl.appendChild(makePageElement(meta.same_name.keyword, '<', prevPage));
    }
    for (let i = startPage; i <= endPage; i++) {
        let el = makePageElement(meta.same_name.keyword, i, i);

        if (i === page) {
            el.classList.remove('btn-outline-primary');
            el.classList.add('btn-primary');
            el.classList.add('on');
            el.click = 'javascript:;';
        }
        paginationEl.appendChild(el);
    }

    if(page < totalPage){
       paginationEl.appendChild(makePageElement(meta.same_name.keyword, '>', endPage + 1));
    }

    return paginationEl;
}

function makePageElement(keyword, text, page){
    let el = document.createElement('a');
    el.classList.add('btn');
    el.classList.add('btn-outline-primary');
    el.href = "#";
    el.innerHTML = text;
    el.onclick = function(){
        kakaoMapSearchKeyword(keyword, searchKeywordCallBack, {sort : 'accuracy', page : page});
    };
    return el;
}
*/
// 검색결과 목록 하단에 페이지번호를 표시는 함수입니다
function getPagination(pagination) {
    let paginationEl = document.createElement('p');
    paginationEl.classList.add('pagination');

    for (let i = 1; i <= pagination.last; i++) {
        let el = document.createElement('a');
        el.classList.add('num');
        el.href = "#";
        el.innerHTML = i;

        if (i===pagination.current) {
            el.classList.add('active');
        } else {
            el.onclick = (function(i) {
                return function() {
                    document.getElementsByClassName('search-result')[0].scrollTop = 0;
                    pagination.gotoPage(i);
                }
            })(i);
        }
        paginationEl.appendChild(el);
    }

    return paginationEl;
}

//선택한 장소 layer item으로 생성
function addUserPickPlaceItemEl(placeInfo){
    //탭 확인 및 추가
    //현재 엑티브 되어있는 탭 확인
    let activeTab = getActiveTabElement();

    //카운트
    let listLen = activeTab.getElementsByClassName('distance_result')[0].getElementsByClassName('item_02').length;

    let itemEl = document.createElement('li');
    itemEl.className = 'item_02';

    let itemNum = document.createElement('span');
    itemNum.className = 'marker_02';
    itemNum.innerHTML = listLen + 1;
    itemEl.appendChild(itemNum);

    let itemContent = document.createElement('div');
    itemContent.className = 'info_02';
    let itemContentStr = '<h5>'+placeInfo.place_name+'</h5>';
    itemContentStr += '<div class="time_wrap">';
    itemContentStr += '     <span>시간대</span>';
    itemContentStr += '     <select class="time_01">';
    for(let i = 0; i < 24; i++){
    itemContentStr += '     <option value="'+i+'">'+(i > 9 ? i : '0'+i)+'</option>';
    }
    itemContentStr += '     </select>';
    itemContentStr += '</div>';
    itemContentStr += '<p class="pagi">';
    itemContentStr += '     <a href="#" class="page_btn btn_up">위로</a>';
    itemContentStr += '<a href="#" class="page_btn btn_down">아래로</a>';
    itemContentStr += '<a href="#" class="page_btn btn_close">닫기</a>';
    itemContentStr += '</p>';

    itemContent.innerHTML = itemContentStr;

    itemEl.appendChild(itemContent);

    activeTab.getElementsByClassName('distance_result')[0].getElementsByTagName('ul')[0].append(itemEl);

    return itemEl;
}

//선택한 목록 중 순서 변경 및 삭제 시 숫자 변경 함수
function changePickPlaceToNumbering(){
    //활성화되어있는 탭
    let activeTab = getActiveTabElement();

    //카운트
    let pickPlaceItemElList = activeTab.getElementsByClassName('distance_result')[0].getElementsByClassName('item_02');

    for(let i = 0; i < pickPlaceItemElList.length; i++){
        pickPlaceItemElList[i].getElementsByClassName('marker_02')[0].innerHTML = i + 1;
    }
}

function changePickPlaceNumberToDrawLine(){
    let activeTabId = getActiveTabElement().id;

    let activePolyLineArr = userPolyline.get(activeTabId);
    //기존 라인 삭제
    if(activePolyLineArr != undefined){
        for(let i = 0; i < activePolyLineArr.length; i++){
            activePolyLineArr[i].setMap(null);
        }
        userPolyline.set(activeTabId, []);
    }
    //라인 다시 그리기
    let activeMarkers = markers.get(activeTabId);
    for(let i = 0; i < activeMarkers.length; i++){
        if(i == activeMarkers.length - 1){
            break;
        }
        let stPoint = activeMarkers[i].mk.getPosition();
        let endPoint = activeMarkers[i+1].mk.getPosition();
        drawLineToMap({stPoint:stPoint, endPoint:endPoint, weight : 2, color : '#dc3545', opacity : 0.8, style : 'solid', endArrow : true, tabId : activeTabId});
    }
}

function changePickPlaceNumberToMarkers(){
    let pickPlaceListEl = $('#userPickPlaceList');//document.getElementById('userPickPlaceList');
    let activeTabId = getActiveTabElement().id;

    //마커 배열 순서 변경
    let newMarkers = [];
    let newOverLays = [];
    let activeOverlays = userOverlay.get(activeTabId);
    $.each(pickPlaceListEl.find('#'+activeTabId+' > .distance_result .item_02'), function(i, v){
        let markerInfo = $(this).data('markerInfo');
        let placeInfo = $(this).data('placeInfo');
        let placeId = $(this).data('placeId');
        newMarkers.push({id : placeId, data : placeInfo, mk : markerInfo});

        for(let j = 0; j < activeOverlays.length; j++){
            if(activeOverlays.length != null && activeOverlays.length != undefined && activeOverlays != ''){
                if(placeId == activeOverlays[j].id){
                    newOverLays.push({id : placeId, ol : activeOverlays[j].ol})
                }
            }
        }
    });

    markers.set(activeTabId, newMarkers);
    userOverlay.set(activeTabId, newOverLays);
}
