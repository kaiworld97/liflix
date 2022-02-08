// window.onload = function () {
//     var img_click = document.getElementById("news_coma");
//     img_click.onclick = news_detail_dialog;
// }

function menudrop(){
    console.log('dropmenu click');
    document.getElementById("dropmenu").classList.toggle("active");
}

$(function(){
    // 	이미지 클릭시 해당 이미지 모달
        $(".news_coma").click(function(){
            $("#news_detail").show();
            // 해당 이미지 가겨오기
            var imgSrc = $(this).children("img").attr("src");
            var imgAlt = $(this).children("img").attr("alt");
            $(".details img").attr("src", imgSrc);
            $(".details img").attr("alt", imgAlt);

            // 해당 이미지 텍스트 가져오기
            var imgTit =  $(this).children("span").text();
            $(".details span").text(imgTit);

       // 해당 이미지에 alt값을 가져와 제목으로
            //$(".modalBox p").text(imgAlt);
        });

        // .modal안에 button을 클릭하면 .modal닫기
        $(".modal button").click(function(){
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