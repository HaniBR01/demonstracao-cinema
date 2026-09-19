# demonstracao-cinema

Projeto web mínimo em Python/Django com apenas a página inicial exibindo `hello world`.

## Como executar no notebook

No notebook (Jupyter/Colab), execute as células abaixo na raiz do projeto:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

Depois, abra no navegador o endereço exibido pelo notebook (porta `8000`).
