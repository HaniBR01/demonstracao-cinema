# demonstracao-cinema

Projeto web em Python/Django para uma experiência de cinema, desenvolvido de forma incremental.

## O que foi feito

- O app `cinema` possui a página inicial e a página do carrinho.
- Lanches podem ser cadastrados pelo Django Admin e vendidos pelo catálogo público.
- O carrinho é persistido no banco e associado à sessão do visitante.
- Cada item do carrinho possui `item_id`, `item_type`, `unit_price` e `quantity`.
- A combinação de tipo e ID identifica um item dentro do carrinho, permitindo reutilizar o mesmo contrato para ingressos, lanches e outros produtos.
- O carrinho calcula a quantidade total e o preço total, permite adicionar e remover itens e valida preço e quantidade.


Exemplo de uso do carrinho:

```python
cart.add_item('42', 'movie_ticket', Decimal('25.00'), quantity=2)
cart.add_item('42', 'snack', Decimal('12.50'))
cart.total_price
```

## TODO incremental

- [x] Implementar catálogo de filmes e sessões.
- [x] Implementar cadastro e venda de lanches.
- [ ] Implementar limitação da quantidade disponível para filmes/sessões e lanches.

A limitação de quantidade disponível fica planejada para uma etapa posterior, conforme a evolução incremental do projeto.

## Como executar

Na raiz do projeto, execute:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

Depois, acesse `http://127.0.0.1:8000/` no navegador.
