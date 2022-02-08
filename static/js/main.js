
function menudrop(){
    console.log('dropmenu click');
    document.getElementById("dropmenu").classList.toggle("active");
}




function close_modal(data){
    document.getElementById(`news_detail${data}`).close();

}

function open_modal(data){
    see_news(data)
    document.getElementById(`news_detail${data}`).showModal();

}

$(function(){
        // 	이미지 클릭시 해당 이미지 모달
        // $(".news_line").click(function() {
        //     $("#news_detail${data}").show();
        // });

        // .modal안에 button을 클릭하면 .modal닫기
        $(".cate_modal button").click(function(){
            $("#news_detail${data}").hide();
        });
    });

function main_close_modal(data){
    document.getElementById(`main_news_detail${data}`).close();

}

function main_open_modal(data){
    see_news(data)
    document.getElementById(`main_news_detail${data}`).showModal();

}

$(function(){
        // 	이미지 클릭시 해당 이미지 모달
        // $(".news_line").click(function() {
        //     $("#news_detail${data}").show();
        // });

        // .modal안에 button을 클릭하면 .modal닫기
        $(".main_modal button").click(function(){
            $("#news_detail${data}").hide();
        });
    });

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


function see_news(data){
        $.ajax({
        type: "POST",
        url: `/news/${data}/`,
        data: {'news_id': data},
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
        }
    });
}