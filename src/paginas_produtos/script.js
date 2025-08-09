let carrinho = JSON.parse(localStorage.getItem('carrinho')) || [];

    function atualizarCarrinho() {
    const itensDiv = document.getElementById('itens-carrinho');
    const totalDiv = document.getElementById('total-carrinho');
    itensDiv.innerHTML = '';
    let total = 0;
    carrinho.forEach((item, idx) => {
        total += item.preco * item.qtd;
        itensDiv.innerHTML += `
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
                <img src="${item.img}" alt="${item.nome}" style="width:50px;height:auto;">
                <div style="display:flex;align-items:center;gap:8px;">
                    <span>${item.nome} - R$${item.preco.toFixed(2)}</span>
                    <button onclick="alterarQtd(${idx}, 1)">+</button>
                    <span>${item.qtd}</span>
                    <button onclick="alterarQtd(${idx}, -1)">-</button>
                </div>
            </div>
        `;
    });
    totalDiv.innerHTML = `<strong>Total: R$${total.toFixed(2)}</strong>`;
    localStorage.setItem('carrinho', JSON.stringify(carrinho));
}

    function alterarQtd(idx, delta) {
    carrinho[idx].qtd += delta;
    if (carrinho[idx].qtd <= 0) carrinho.splice(idx, 1);
    atualizarCarrinho();
}

document.querySelectorAll('.add-carrinho').forEach(btn => {
    btn.addEventListener('click', () => {
        const nome = btn.dataset.nome;
        const preco = parseFloat(btn.dataset.preco);
        const img = btn.dataset.img;
        const idx = carrinho.findIndex(i => i.nome === nome);
        if (idx > -1) {
            carrinho[idx].qtd++;
        } else {
            carrinho.push({ nome, preco, qtd: 1, img });
        }
        document.getElementById('sidebar-carrinho').classList.add('aberta');
        atualizarCarrinho();
    });
});

document.getElementById('fechar-carrinho').onclick = () => {
    document.getElementById('sidebar-carrinho').classList.remove('aberta');
};

document.getElementById('ver-carrinho-btn').onclick = () => {
    // O carrinho já está salvo no localStorage
    window.open('carrinho.html', '_blank');
};

document.getElementById('comprar-btn').onclick = () => {
    alert('Compra realizada!');
    carrinho.length = 0;
    atualizarCarrinho();
    document.getElementById('sidebar-carrinho').classList.remove('aberta');
};

// Atualiza o carrinho ao carregar a página
atualizarCarrinho();