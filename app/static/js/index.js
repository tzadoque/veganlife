function hideShowPassword(id) {
  input = document.getElementById(id)
  if( input.type === "password") {
    input.type = "text";
  } else {
    input.type = "password"
  }
}

function toggleMenu(id) {
  menu = document.querySelector(`#${id}`)
  menu.classList.toggle("active")
}

function loadFile(event) {
  var image = document.getElementById('output');
  image.src = URL.createObjectURL(event.target.files[0]);
  imagem = document.querySelector('#image')
};