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
        document.getElementById("login").classList.add("hidden");
        document.getElementById("solicitacao").classList.remove("hidden");
        alert("Login realizado com sucesso!");
    } else {
        alert("Erro no login: " + (data.detail || "Verifique CPF e senha"));
    }
}

async function enviarSolicitacao() {
    const token = localStorage.getItem("token");
    if (!token) {
        alert("Faça login novamente.");
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
        alert("Solicitação enviada com sucesso!");
    } else {
        alert("Erro: " + (data.detail || "Erro desconhecido"));
    }
}

function logout() {
    localStorage.removeItem("token");
    location.reload();
}

function checarLogin() {
    const token = localStorage.getItem("token");
    if (token) {
        document.getElementById("login").classList.add("hidden");
        document.getElementById("solicitacao").classList.remove("hidden");
    } else {
        document.getElementById("login").classList.remove("hidden");
        document.getElementById("solicitacao").classList.add("hidden");
    }
}

window.onload = checarLogin;