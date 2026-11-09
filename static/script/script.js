console.log(window.location.pathname);

function redirecionarParaRegistro() {
   
}

if (window.location.pathname === "/") {
document.getElementById("redirecionar").addEventListener("click", function() {
    window.location.href = "/registrar";
} );}

if (window.location.pathname === "/index") {
document.getElementById("registrar_animal").addEventListener("click", function() {
    window.location.href = "/registrar_animal";
});}