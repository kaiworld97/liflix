
function menudrop(){
    console.log('dropmenu click');
    document.getElementById("dropmenu").classList.toggle("active");
}




function close_modal(data){
    console.log('bye')
    document.getElementById(`news_detail${data}`).close();

}

function open_modal(data){
    console.log('hi')
    document.getElementById(`news_detail${data}`).showModal();

}

$(function(){
        // 	이미지 클릭시 해당 이미지 모달
        $(".news_line").click(function() {
            $("#news_detail${data}").show();
        });

        // .modal안에 button을 클릭하면 .modal닫기
        $(".modal button").click(function(){
            $("#news_detail${data}").hide();
        });

    });



