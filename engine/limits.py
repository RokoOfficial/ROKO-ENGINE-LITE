"""
Limites de segurança do motor ROKO Script.
"""

MAX_SCRIPT_LINES = 10000
MAX_WHILE_ITERATIONS = 5000
MAX_LOOP_TOTAL_STEPS = 50000   # teto global de passos de laço por execução (FOR+WHILE somados)
MAX_BLOCK_DEPTH = 64           # profundidade máxima de aninhamento IF/WHILE/FOR
MAX_EXEC_SECONDS = 60          # teto de tempo de execução de um script
