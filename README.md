# demonstracao-cinema

Projeto web mínimo em Python/Django com apenas a página inicial exibindo `hello world`.

## Carrinho genérico

O app `cart` armazena linhas sem conhecer o catálogo. Cada linha possui `item_id`, `item_type`, `unit_price` e `quantity`; a combinação de tipo e ID identifica um item dentro do carrinho. Assim, ingressos, lanches ou qualquer outro produto podem usar o mesmo contrato.

Exemplo de uso:

```python
cart.add_item('42', 'movie_ticket', Decimal('25.00'), quantity=2)
cart.add_item('42', 'snack', Decimal('12.50'))
cart.total_price
```

## Como executar no notebook

No notebook (Jupyter/Colab), execute as células abaixo na raiz do projeto:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

Depois, abra no navegador o endereço exibido pelo notebook (porta `8000`).
