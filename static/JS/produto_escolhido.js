ScrollReveal().reveal(`.campo`,{duration:2000});



// Função para simular a busca e exibição de comentários (a ser implementada)
function buscarComentarios() {
    // Buscar comentários do servidor ou banco de dados
    const comentarios = [
        { nome: "João Silva", comentario: "Adorei o site! Muito fácil de usar." },
        { nome: "Maria Oliveira", comentario: "Conteúdo excelente! Aprendi muito por aqui." },
        { nome: "Pedro Souza", comentario: "Parabéns pelo trabalho! Recomendo a todos." }
    ];

    // Limpar lista de comentários existentes
    const listaComentarios = document.querySelector('.espaco-comentarios ul');
    listaComentarios.innerHTML = '';

    // Exibir cada comentário na lista
    comentarios.forEach(comentario => {
        const novoComentario = document.createElement('li');
        novoComentario.classList.add('comentario');

        const nome = document.createElement('strong');
        nome.textContent = comentario.nome + ': ';

        const textoComentario = document.createTextNode(comentario.comentario);

        novoComentario.appendChild(nome);
        novoComentario.appendChild(textoComentario);

        listaComentarios.appendChild(novoComentario);
    });
}

// Chamar a função para buscar comentários na inicialização da página
buscarComentarios();
