var mainMap;
var zoomControl;
var geocoder;
var searchMarkers = [];
var mkPlaceOverlay = '';
var mobilePlaceOverlay = '';
var markers = new Map();
var userPolyline = new Map();
var userOverlay = new Map();
var csrf_token = '';

$(document).ready(function(){
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });
    //높이 계산
    let totalHeight = window.innerHeight-101-78-50;
    let searchDiv = $('.search-result').css('height', totalHeight);

    /* 메뉴버튼을 눌렀을때, 오버레이부분을 클릭했을때*/
    $(".menu_button, .panel-overlay").click( function() {
        $(".menu_button, .panel-overlay, .head_top_menu").toggleClass("active"); //해당 영역에 toggleClass를 넣어줍니다
        /* panel overlay가 활성화 되어있는지를 체크합니다. */
        if ($(".panel-overlay").hasClass("active")) {
            $(".panel-overlay").fadeIn();
        } else {
            $(".panel-overlay").fadeOut();
        }
    });

    $(window).resize(function(){
        let totalHeight = window.innerHeight-78-101-50;
        $('.search-result').css('height', totalHeight);
    });

    $('#analysisStModal #telno').autoHypenPhone();

    if($('#mainMap').length > 0){
        kakaoMapInit();
    }
})

function removeAllChildNodes(ele){
    while(ele.hasChildNodes()){
        ele.removeChild(ele.lastChild);
    }
}

function getActiveTabElement(){
    return document.getElementById('dateTab-content').getElementsByClassName('active')[0];
}

function isMobile(){
    let mIs = false;
    if(navigator.platform){
        if("win16|win32|win64|mac|macintel".indexOf(navigator.platform.toLowerCase()) < 0){
            mIs = true;
        }
    }
    return mIs;
}

function getDate(standardDate, type1, dateType, num){
    let date = standardDate.split('-');
    let year = date[0];
    let month = date[1];
    let days = date[2];
    date = new Date(Number(year), Number(month) - 1, Number(days));
    if(type1 == 'plus'){
        if(dateType == 'year'){
            date.setFullYear(date.getFullYear() + num);
        } else if(dateType == 'month'){
            date.setMonth(date.getMonth() + num);
        } else {
            date.setDate(date.getDate() + num);
        }
    } else {
        if(dateType == 'year'){
            date.setFullYear(date.getFullYear() - num);
        } else if(dateType == 'month'){
            date.setMonth(date.getMonth() - num);
        } else {
            date.setDate(date.getDate() - num);
        }
    }

    return date;
}

$.fn.serializeObject = function () {
    'use strict';
    var result = {};
    var extend = function (i, element) {
        var node = result[element.name];
        if ('undefined' !== typeof node && node !== null) {
            if ($.isArray(node)) {
                node.push(element.value);
            } else {
                result[element.name] = [node, element.value];
            }
        } else {
          result[element.name] = element.value;
        }
    };

    $.each(this.serializeArray(), extend);
    return result;
};

Date.prototype.format = function (f) {
    if (!this.valueOf()) return " ";

    var weekKorName = ["일요일", "월요일", "화요일", "수요일", "목요일", "금요일", "토요일"];
    var weekKorShortName = ["일", "월", "화", "수", "목", "금", "토"];
    var weekEngName = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    var weekEngShortName = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    var d = this;

    return f.replace(/(yyyy|yy|MM|dd|KS|KL|ES|EL|HH|hh|mm|ss|a\/p)/gi, function ($1) {
        switch ($1) {
            case "yyyy": return d.getFullYear(); // 년 (4자리)
            case "yy": return (d.getFullYear() % 1000).zf(2); // 년 (2자리)
            case "MM": return (d.getMonth() + 1).zf(2); // 월 (2자리)
            case "dd": return d.getDate().zf(2); // 일 (2자리)
            case "KS": return weekKorShortName[d.getDay()]; // 요일 (짧은 한글)
            case "KL": return weekKorName[d.getDay()]; // 요일 (긴 한글)
            case "ES": return weekEngShortName[d.getDay()]; // 요일 (짧은 영어)
            case "EL": return weekEngName[d.getDay()]; // 요일 (긴 영어)
            case "HH": return d.getHours().zf(2); // 시간 (24시간 기준, 2자리)
            case "hh": return ((h = d.getHours() % 12) ? h : 12).zf(2); // 시간 (12시간 기준, 2자리)
            case "mm": return d.getMinutes().zf(2); // 분 (2자리)
            case "ss": return d.getSeconds().zf(2); // 초 (2자리)
            case "a/p": return d.getHours() < 12 ? "오전" : "오후"; // 오전/오후 구분
            default: return $1;
        }
    });
};

String.prototype.string = function (len) { var s = '', i = 0; while (i++ < len) { s += this; } return s; };
String.prototype.zf = function (len) { return "0".string(len - this.length) + this; };
Number.prototype.zf = function (len) { return this.toString().zf(len); };

(function($){
	$.fn.autoHypenPhone = function(options){
		this.each(function(){
			var $id = $(this);
			var tmp = '';
			$id.keyup(function(){
				var str = $(this).val();
				$id.val(autoHypenPhoneString(str));
			});
			$id.change(function(){
				var str = $(this).val();
				$id.val(autoHypenPhoneString(str));
			});
		});
		function autoHypenPhoneString(str){
			str = str.replace(/[^0-9]/g, '');
			var tmp = '';
			var c = (str.substr(0, 2) == "02") ? 1 : 0;
			if( str.length < (4 - c)){
				return str;
			}else if(str.length < (7 - c)){
				tmp += str.substr(0, (3 - c));
				tmp += '-';
				tmp += str.substr((3 - c));
				return tmp;
			}else if(str.length < (11 - c)){
				tmp += str.substr(0, (3 - c));
				tmp += '-';
				tmp += str.substr((3 - c), 3);
				tmp += '-';
				tmp += str.substr((6 - c));
				return tmp;
			}else{
				tmp += str.substr(0, (3 - c));
				tmp += '-';
				tmp += str.substr((3 - c), 4);
				tmp += '-';
				tmp += str.substr((7 - c), 4);
				return tmp;
			}
		}
	};
})(jQuery);