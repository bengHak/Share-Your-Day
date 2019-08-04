// 입력값을 maxlength 주기 위한 함수
function maxLengthCheck(object){
    if (object.value.length > object.maxLength){
        object.value = object.value.slice(0, object.maxLength);
    }    
}

// 생년월일을 오늘로 설정하기 위한 함수
document.getElementById('birthday').value = new Date().toISOString().substring(0, 10);

