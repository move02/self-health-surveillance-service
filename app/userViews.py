from flask import Flask, jsonify, redirect, render_template, request, flash, url_for
from app import app, db, bcrypt, json
from .models.user.placeInfo import searchKeword, pickPlace, placeInfo
from .models.user.userInfo import userInfo, userSchdul, userLocation
from collections import OrderedDict

@app.route("/map")
def maps():
    return render_template("user/map.html", title="참여형 역학조사 시스템")

@app.route("/loadUserInfoToAnalysisList", methods=['POST'])
def loadUserInfoToAnalysisList():
    resultStatus = "success"
    resultMessage = ""
    resultData = []
    jsonData = request.get_json()
    try:
        resideArea = jsonData['e_reside_area']
        sexdstn = jsonData['e_sexdstn']
        agrde = jsonData['e_agrde']
        email = jsonData['e_email']
        password = jsonData['e_password']
        queryData = db.session.query(userSchdul, userInfo.password)\
                                    .join(userInfo, userSchdul.userSn == userInfo.sn)\
                                    .filter(userInfo.resideArea == resideArea,
                                            userInfo.sexdstn == sexdstn,
                                            userInfo.agrde == agrde,
                                            userInfo.email == email)\
                                    .all()

        for nonPasswordInfo in queryData:
            if bcrypt.check_password_hash(nonPasswordInfo.password, password):
                resultData.append(nonPasswordInfo.userSchdul.toDict())

    except Exception as e:
        print(e)
        resultStatus = "fail"
        resultMessage = "사용자 이동경로 분석목록 호출 시 에러발생"

    return jsonify(status=resultStatus, message=resultMessage, data=resultData)

@app.route("/loadUserInfo", methods=['POST'])
def loadUserInfo():
    resultStatus = "success"
    resultMessage = ""
    resultData = []
    jsonData = request.get_json()
    try:
        sn = jsonData['sn']
        queryData = db.session.query(userSchdul.stdde, userLocation.deOrdr, userLocation.visitTime
                                    , userLocation.coursOrdr, placeInfo)\
                                .join(placeInfo, userLocation.placeId == placeInfo.placeId)\
                                .join(userSchdul, userLocation.schdulSn == userSchdul.sn)\
                                .filter(userLocation.schdulSn == sn)\
                                .all()
        maxDeOrdr = db.session.query(db.func.max(userLocation.deOrdr))\
                                .filter(userLocation.schdulSn == sn)\
                                .scalar()

        for data in queryData:
            datas = {}
            datas['stdde'] = data.stdde
            datas['deOrdr'] = data.deOrdr
            datas['visitTime'] = data.visitTime
            datas['coursOrdr'] = data.coursOrdr
            datas['placeInfo'] = data.placeInfo.toDict()
            resultData.append(datas)

    except Exception as e:
        print(e)
        resultStatus = "fail"
        resultMessage = "사용자 이동경로 호출 시 에러발생"

    return jsonify(status=resultStatus, message=resultMessage, data=resultData, maxDeOrdr=maxDeOrdr)

@app.route("/keyword/save", methods=['POST'])
def searchKeywodSave():
    resultStatus = "success"
    try:
        keywordJsonData = request.get_json()
        type = keywordJsonData['searchType']
        keyword = keywordJsonData['keyword']
        searchKewordModel = searchKeword(type, keyword)
        db.session.add(searchKewordModel)
        db.session.commit()
    except:
        resultStatus = "fail"

    return jsonify(status=resultStatus)

@app.route("/pickPlace/save", methods=['POST'])
def pickPlaceSave():
    resultStatus = "success"
    resultMessage = ""
    try:
        jsonData = request.get_json()
        place_id = jsonData['place_id']
        place_name = jsonData['place_name']
        place_address = jsonData['place_address']
        place_road_address = jsonData['place_road_address']
        lat = jsonData['lat']
        lng = jsonData['lng']
        place_ctprvn = jsonData['place_ctprvn']
        place_signgu = jsonData['place_signgu']

        #장소 선택 히스토리 저장
        pickPlaceModel = pickPlace(place_id, place_name, place_address, place_road_address, lat, lng, place_ctprvn, place_signgu)
        db.session.add(pickPlaceModel)
        db.session.commit()
    except:
        resultStatus = "fail"
        resultMessage = "장소 선택 히스토리 저장 중 에러발생"
    else:
        try:
            #장소 정보 저장
            #장소 아이디를 비교해서 없을 시 저장
            exists = db.session.query(placeInfo.placeId).filter_by(placeId=place_id).scalar()
            if exists == None:
                placeInfoModel = placeInfo(place_id, place_name, place_address, place_road_address, lat, lng, place_ctprvn, place_signgu)
                db.session.add(placeInfoModel)
                db.session.commit()
        except:
            resultStatus = "fail"
            resultMessage = "장소 정보 저장 시 에러발생"

    return jsonify(status=resultStatus, message=resultMessage)

@app.route("/analysis/userInfo/save", methods=['POST'])
def analysisOkUserInfoSave():
    resultStatus = "success"
    resultMessage = ""
    jsonData = request.get_json()
    try:
        reside_area = jsonData['reside_area']
        sexdstn = jsonData['sexdstn']
        telno = jsonData['telno']
        password = jsonData['password']
        delete_at = 'N'
        email = jsonData['email']
        agrde = jsonData['agrde']
        userInfo_M = userInfo(reside_area, sexdstn, telno, password, delete_at, email, agrde)
        userInfo_M.set_password(password)
        exists = db.session.query(userInfo.sn, userInfo.password).filter_by(resideArea=reside_area, deleteAt=delete_at,
                                                                            sexdstn=sexdstn, telno=telno,
                                                                            email=email, agrde=agrde).first()
        if exists == None:
            db.session.add(userInfo_M)
            db.session.flush()
        else:
            if bcrypt.check_password_hash(exists.password, password):
                userInfo_M.sn = exists.sn
            else:
                db.session.add(userInfo_M)
                db.session.flush()
    except Exception as e:
        print(e)
        resultStatus = "fail"
        resultMessage = "사용자 정보 저장 시 에러발생"

    #사용자 일정 정보 저장
    try:
        # db.session.query(t_idrs_user_info_m01.SN).first().order_by(t_idrs_user_info_m01.REGIST_DATE.desc())
        userSn = userInfo_M.sn
        stdde = jsonData['baseDate']
        userInfo_S = userSchdul(userSn, stdde)
        db.session.add(userInfo_S)
        db.session.flush()
    except:
        resultStatus = "fail"
        resultMessage = "사용자 일정 저장 시 에러발생"

    #사용자 이동경로 저장
    try:
        schdulSn = userInfo_S.sn
        for lo_info in jsonData['location']:
            deOrdr = lo_info['deOrdr']
            coursOrdr = lo_info['coursOrdr']
            visitTime = lo_info['visitTime']
            visitDate = lo_info['coursDate']
            placeId = lo_info['place_id']
            userInfo_L = userLocation(schdulSn, deOrdr, visitTime, visitDate, placeId, coursOrdr)
            db.session.add(userInfo_L)
            db.session.commit()
    except Exception as e:
        print(e)
        resultStatus = "fail"
        resultMessage = "사용자 이동경로 저장 시 에러발생"

    return jsonify(status=resultStatus, message=resultMessage)

# @app.route("/analysis/userInfo", methods=['POST'])
# def analysisUserInfo():
#
#     return 'success'
