# Missão Dengue — A* com terrenos ponderados

Uma criança atravessa um acampamento ecológico para eliminar a água parada de
um pneu. O A* considera grama com custo 1, lama com custo 3 e os objetos como
obstáculos.

```bash
python3 -m pip install -r requirements.txt
python3 main.py
```

Um mapa aleatório com solução garantida é criado em cada execução. **Espaço**
inicia/pausa, **A** seleciona A*, **G** seleciona a busca gulosa, **R** reinicia
o mapa atual, **N** gera outro mapa e **Esc** sai. É possível alternar entre A*
e gulosa sem mudar o mapa, permitindo comparar as rotas encontradas.
Para testar o algoritmo:

```bash
python3 -m unittest -v
```
