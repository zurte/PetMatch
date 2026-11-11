console.log(window.location.pathname);

if (window.location.pathname === "/") {
document.getElementById("redirecionar").addEventListener("click", function() {
    window.location.href = "/registrar";
} );}

if (window.location.pathname === "/index") {
document.getElementById("registrar_animal").addEventListener("click", function() {
    window.location.href = "/registrar_animal";
});}

if (window.location.pathname === "/formulario_registro") {
    document.getElementById("formulario_usuario").addEventListener("click", function() {
        fetch("/adicionar_usuario", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                nome: document.getElementById("nome").value,
                email: document.getElementById("email").value,
                senha: document.getElementById("senha").value,
                cep: document.getElementById("cep").value,
                idade: document.getElementById("idade").value,
                numero: document.getElementById("numero").value,
            })
        });
    });
}