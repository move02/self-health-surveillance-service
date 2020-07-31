const passwordRegex = new RegExp("[0-9]{4}");
var isUniqueId = false;
var isPasswordValid = false;
var isPasswordMatch = false;

// 유효 패스워드 확인
$("#input-password").keyup(function () {
    let pwVal = $(this).val();
    let pwValidBadge = $("#password-valid-badge");
    let pwConfirmVal = $("#input-confirm-password").val();
    let pwConfirmBadge = $("#password-confirm-badge");
    if(passwordRegex.test(pwVal)){
        pwValidBadge.removeClass("badge-light");
        pwValidBadge.removeClass("badge-danger");
        pwValidBadge.addClass("badge-success");
        pwValidBadge.text("안전");
        isPasswordValid = true;
    } else{
        pwValidBadge.removeClass("badge-light");
        pwValidBadge.removeClass("badge-success");
        pwValidBadge.addClass("badge-danger");
        pwValidBadge.text("불안");
        isPasswordValid = false;
    }
    confirmPw(pwVal, pwConfirmVal, pwConfirmBadge);
});


$("#input-username").keyup(function(){
    let uniqueIdBadge = $("#unique-username-badge");
    if(isUniqueId){
        isUniqueId = false;
        uniqueIdBadge.toggleClass("text-warning", true);
        uniqueIdBadge.toggleClass("text-danger", false);
        uniqueIdBadge.toggleClass("text-success", false);
        uniqueIdBadge.text("아이디 중복확인을 해주세요.");
    }
});

// 패스워드 및 패스워드 확인
$("#password-confirm").keyup(function () {
    let pwVal = $("#emplyrPassword").val();
    let pwConfirmVal = $(this).val();
    let pwConfirmBadge = $("#password-confirm-badge");
    confirmPw(pwVal, pwConfirmVal, pwConfirmBadge)
});

// 아이디 중복체크
$("#check-username-overlap").click(function(){
    let inputUsername = $("#input-username").val();
    let uniqueIdBadge = $("#unique-username-badge");
    $.ajax({
        url:"/admin/check/username",
        method: "POST",
        headers: {
            "X-CSRFToken": csrf_token,
            "Content-type": "application/json"
        },
        data:{
            inputUsername : inputUsername
        },
        success:function(data){
            //로직
            if(data['isunique'] === "true"){
                isUniqueId = true;
                uniqueIdBadge.toggleClass("text-warning", false);
                uniqueIdBadge.toggleClass("text-danger", false);
                uniqueIdBadge.toggleClass("text-success", true);
                uniqueIdBadge.text("사용 가능한 id입니다.");
            } else {
                isUniqueId = false;
                uniqueIdBadge.toggleClass("text-warning", false);
                uniqueIdBadge.toggleClass("text-danger", true);
                uniqueIdBadge.toggleClass("text-success", false);
                uniqueIdBadge.text("이미 사용중인 id입니다.");
            }
        }
    })
});

function confirmPw(pwVal, pwConfirmVal, pwConfirmBadge){
    if(pwVal === pwConfirmVal){
        pwConfirmBadge.removeClass("badge-light");
        pwConfirmBadge.removeClass("badge-danger");
        pwConfirmBadge.addClass("badge-success");
        pwConfirmBadge.text("일치");
        isPasswordMatch = true;
    } else{
        pwConfirmBadge.removeClass("badge-light");
        pwConfirmBadge.removeClass("badge-success");
        pwConfirmBadge.addClass("badge-danger");
        pwConfirmBadge.text("불일치");
        isPasswordMatch = false;
    }
}