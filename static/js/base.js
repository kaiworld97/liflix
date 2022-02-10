// window.onload = function () {
//     var img_click = document.getElementById("news_coma");
//     img_click.onclick = news_detail_dialog;
// }

function menudrop() {
    console.log('dropmenu click');
    document.getElementById("dropmenu").classList.toggle("active");
}

$(function () {
    // 	이미지 클릭시 해당 이미지 모달
    $(".news_coma").click(function () {
        $("#news_detail").show();
        // 해당 이미지 가겨오기
        var imgSrc = $(this).children("img").attr("src");
        var imgAlt = $(this).children("img").attr("alt");
        $(".details img").attr("src", imgSrc);
        $(".details img").attr("alt", imgAlt);

        // 해당 이미지 텍스트 가져오기
        var imgTit = $(this).children("span").text();
        $(".details span").text(imgTit);

        // 해당 이미지에 alt값을 가져와 제목으로
        //$(".modalBox p").text(imgAlt);
    });

    // .modal안에 button을 클릭하면 .modal닫기
    $(".modal button").click(function () {
        $(".modal").hide();
    });

    //.modal밖에 클릭시 닫힘
    $("#news_detail").click(function (e) {
        if (e.target.className != "modal") {
            return false;
        } else {
            $("#news_detail").hide();
        }
    });
});

$(document).ready(function () {

    $('.nav .sub_1').hide();

    $('.nav_item').mouseover(function () {
        $('.sub_1').slideDown();

    });
    $('.nav_item').mouseleave(function () {
        $('.sub_1').hide();
    });
});


// 블루

var isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);

if (!isChrome) {
    document.getElementsByClassName('infinityChrome')[0].style.display = "none";
    document.getElementsByClassName('infinity')[0].style.display = "block";
}

function ai_close_btn() {
    document.querySelector(".ai_text").innerHTML = ""
    document.getElementById('ai_div').classList.add('visibility_hidden')
    blue = false
}

function speak(text) {
    if (typeof SpeechSynthesisUtterance === "undefined" || typeof window.speechSynthesis === "undefined") {
        alert("이 브라우저는 음성 합성을 지원하지 않습니다.")
        return
    }

    window.speechSynthesis.cancel() // 현재 읽고있다면 초기화


    const speechMsg = new SpeechSynthesisUtterance()
    speechMsg.rate = 1 // 속도: 0.1 ~ 10
    speechMsg.pitch = 1 // 음높이: 0 ~ 2
    speechMsg.lang = "ko-KR"
    speechMsg.text = text

    // SpeechSynthesisUtterance에 저장된 내용을 바탕으로 음성합성 실행
    window.speechSynthesis.speak(speechMsg)
}


let blue = false

window.SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

// 인스턴스 생성
const recognition = new SpeechRecognition();

// true면 음절을 연속적으로 인식하나 false면 한 음절만 기록함
recognition.interimResults = true;
// 값이 없으면 HTML의 <html lang="en">을 참고합니다. ko-KR, en-US
recognition.lang = "ko-KR";
// true means continuous, and false means not continuous (single result each time.)
// true면 음성 인식이 안 끝나고 계속 됩니다.
recognition.continuous = false;
// 숫자가 작을수록 발음대로 적고, 크면 문장의 적합도에 따라 알맞은 단어로 대체합니다.
// maxAlternatives가 크면 이상한 단어도 문장에 적합하게 알아서 수정합니다.
recognition.maxAlternatives = 10000;


let speechToText = "";


recognition.addEventListener("result", (e) => {
    let interimTranscript = "";
    let last = ''
    for (let i = e.resultIndex, len = e.results.length; i < len; i++) {
        let transcript = e.results[i][0].transcript;
        console.log('transcript', transcript);
        last = transcript

        if (e.results[i].isFinal) {
            speechToText += transcript;
        } else {
            interimTranscript += transcript;
        }
    }
    console.log('speechToText', speechToText);
    console.log('interimTranscript', interimTranscript);
    document.querySelector(".ai_text").innerText = last;
    if (interimTranscript == '블루' && blue == false) {
        document.getElementById('ai_div').classList.remove('visibility_hidden')
        console.log('블루 켜짐!')
        blue = true
        setTimeout(() => speak('안녕하세요'), 500);
    }
});

// 음성인식이 끝나면 자동으로 재시작합니다.


recognition.addEventListener("end", (e) => {
    // recognition.start();
    console.log('bye')
    let ai_text = document.querySelector(".ai_text")
    console.log(ai_text.innerText)
    if (blue === true) {
        switch (ai_text.innerText) {
            case "홈 가줘":
            case "홈가 줘":
                ai_close_btn()
                location.href = '/'
                break
            case '새로고침 해 줘':
                speak('페이지를 새로고침합니다')
                window.location.reload()
                break
            case '안녕':
                setTimeout(() => speak('안녕하세요'), 1000);
                document.querySelector(".ai_text").innerHTML = ""
                break
            case '누가 만들었어':
            case '너는 누가 만들었어':
                setTimeout(() => speak('홍채영님이 만들었습니다'), 1000);
                document.querySelector(".ai_text").innerHTML = ""

                break
            case '너는 누구야':
            case '누구야':
            case '넌 누구야':
                setTimeout(() => speak('저는 블루 입니다'), 1000);
                document.querySelector(".ai_text").innerHTML = ""

                break
            case '인사해':
            case '블루 인사해':
                setTimeout(() => speak('내배캠 여러분 안녕하세요 저는 블루 입니다'), 1000);
                document.querySelector(".ai_text").innerHTML = ""
                break
            case '블루 사라져':
            case '사라져':
                speak('안녕히 계세요')
                ai_close_btn()
                break
            case '정치 카테고리가 줘':
                ai_close_btn()
                location.href = '/news/100'
                break
            case '생활문화 카테고리가 줘':
                ai_close_btn()
                location.href = '/news/103'
                break
            case '세계 카테고리가 줘':
                ai_close_btn()
                location.href = '/news/104'
                break
            case '사회 카테고리가 줘':
                ai_close_btn()
                location.href = '/news/102'
                break
            case 'it 과학 카테고리가 줘':
                ai_close_btn()
                location.href = '/news/105'
                break
            case '경제 카테고리가 줘':
                ai_close_btn()
                location.href = '/news/103'
                break
            // case '게시판가 줘':
            //     setTimeout(() => speak('저는 블루 입니다'), 1000);
            //     ai_close_btn()
            //     location.href = '/'
            //     break
            default:
                if ((ai_text.innerText).split(' ').includes('추천해')) {
                    document.getElementById('blue').value = ai_text.innerText
                    document.getElementById('blue_btn').click()
                    ai_close_btn()
                }
        }
    }
    recognition.start()

});

// 음성 인식 시작
recognition.start();
console.log('hi')

function movie_click(){
    document.getElementById('blue').value = '영화 추천해 줘'
    document.getElementById('blue_btn').click()
}
function news_click(){
    document.getElementById('blue').value = '뉴스 추천해 줘'
    document.getElementById('blue_btn').click()
}
