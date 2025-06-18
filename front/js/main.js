const API_URL = "http://127.0.0.1:8000";

function atualizarFormulario() {
    const tipo = document.getElementById("tipo").value;
    document.getElementById("campos-uber").classList.add("hidden");
    document.getElementById("campos-entregador").classList.add("hidden");
    document.getElementById("campos-visitante").classList.add("hidden");

    if (tipo === "uber") {
        document.getElementById("campos-uber").classList.remove("hidden");
    } else if (tipo === "delivery") {
        document.getElementById("campos-entregador").classList.remove("hidden");
    } else if (tipo === "guest") {
        document.getElementById("campos-visitante").classList.remove("hidden");
    }
}

async function login() {
    const cpf = document.getElementById("cpf").value;
    const password = document.getElementById("password").value;

    const res = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cpf, password })
    });

    const data = await res.json();

    if (res.ok) {
        localStorage.setItem("token", data.access_token);
        window.location.href = "home.html";
    } else {
        alert("Erro no login: " + (data.detail || "Verifique CPF e senha"));
    }
}

async function enviarSolicitacao() {
    const token = localStorage.getItem("token");
    if (!token) {
        alert("Faça login novamente.");
        window.location.href = "index.html";
        return;
    }

    const payload = {
        access_type: document.getElementById("tipo").value,
        name: document.getElementById("nome").value,
        address: document.getElementById("endereco").value,
        user: document.getElementById("solicitante").value,
        license_plate: document.getElementById("placa").value,
        establishment: document.getElementById("empresa").value,
        is_driving: document.getElementById("is_driving").checked
    };

    const res = await fetch(`${API_URL}/order/request-access`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (res.ok) {
        window.location.href = "sucesso.html";
    } else {
        alert("Erro: " + (data.detail || "Erro desconhecido"));
    }
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "index.html";
}

function checarLogin() {
    const token = localStorage.getItem("token");
    const loginContainer = document.getElementById("login");
    const solicitacaoContainer = document.getElementById("solicitacao");

    if (token) {
        if (loginContainer) loginContainer.classList.add("hidden");
        if (solicitacaoContainer) solicitacaoContainer.classList.remove("hidden");
    } else {
        if (loginContainer) loginContainer.classList.remove("hidden");
        if (solicitacaoContainer) solicitacaoContainer.classList.add("hidden");
    }
}

window.onload = checarLogin;
