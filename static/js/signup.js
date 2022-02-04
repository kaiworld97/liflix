
function loadFile(input) {

    // let file_name = input.files[0]['name']
    let file = input.files[0];
    let file_img = document.createElement("img");
    file_img.setAttribute("class", 'img')
    file_img.src = URL.createObjectURL(file);

    file_img.style.width = "100px";
    file_img.style.height = "100px";
    file_img.style.visibility = "visible";
    file_img.style.objectFit = "cover";


    document.getElementById('btn').classList.add('hidden')
    document.getElementById('selectFile').classList.add('hidden')

    let container = document.getElementById("profileimg");

    container.style.width = "100px";
    container.appendChild(file_img);


}



