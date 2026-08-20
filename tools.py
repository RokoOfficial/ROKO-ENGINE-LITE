#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
ROKO ROUTER — tools.py
================================================================================
Registro de ferramentas (tools): implementação de cada ferramenta nativa
(RokoTools), a especificação TOOL_SPECS usada pelo motor ROKO Script e pela
API HTTP, as ferramentas meta.* (introspecção) e o executor genérico
execute_tool().

Este arquivo NÃO depende de roko.py nem de api.py — é a camada mais baixa
(só usa a biblioteca padrão + requests). roko.py importa `execute_tool`
daqui para resolver instruções CALL; api.py importa as funções meta_* e
TOOL_SPECS para expor os endpoints /tools, /tool/<nome>, etc.

Separar os nomes/implementações das ferramentas neste arquivo próprio foi
um pedido explícito: manter a lista de ferramentas isolada do motor da
linguagem e da camada HTTP torna muito mais fácil adicionar, remover ou
ajustar uma ferramenta sem precisar entender (ou arriscar quebrar) o
parser/interpretador ou as rotas da API.
================================================================================
"""
from __future__ import annotations

import ast
import datetime as dt
import hashlib
import inspect
import json
import math
import os
import random
import re
import sys
import time
import unicodedata
import uuid
from typing import Any, Callable, Dict, List, Optional, Union

import requests

# Versão exposta por meta.info() — mantida aqui porque é sobre as ferramentas,
# não sobre o motor da linguagem nem sobre a API HTTP.
TOOL_VERSION = "1.0.0"

# Estas três constantes também existem em router.py (fonte de verdade para a
# aplicação como um todo). Duplicadas aqui de propósito: tools.py precisa
# funcionar de forma 100% independente (importável e testável sozinho, sem
# depender de router.py ou api.py) — é exatamente o ponto de separar os
# nomes/implementações das ferramentas num arquivo próprio. Se você mudar
# REQUEST_TIMEOUT/APP_NAME/APP_VERSION em router.py, replique aqui também.
REQUEST_TIMEOUT = 30  # segundos, usado pelas ferramentas http.*
APP_NAME = "ROKO ROUTER"
APP_VERSION = "2.1.0"
API_VERSION = "v1"

# Idem para o diretório de logs — RokoTools.log_print() precisa gravar em
# disco de forma independente de router.py (ver nota acima sobre
# duplicação intencional de constantes de infraestrutura).
from pathlib import Path as _Path
LOGS_FOLDER = _Path(__file__).resolve().parent / "logs"
LOGS_FOLDER.mkdir(parents=True, exist_ok=True)


class RokoTools:
    """
    Classe contendo todas as ferramentas disponíveis na API ROKO ROUTER.

    Cada ferramenta é um método estático que recebe parâmetros tipados e
    retorna um resultado processado. As ferramentas são organizadas por
    categorias: matemática, strings, listas, JSON, datas, HTTP, criptografia,
    aleatório, log e sistema.
    """

    # ------------------------------------------------------------------------
    # CATEGORIA: MATEMÁTICA
    # ------------------------------------------------------------------------

    @staticmethod
    def math_sum(a: Union[int, float], b: Union[int, float]) -> float:
        """
        Soma dois números.

        Args:
            a (int|float): Primeiro número
            b (int|float): Segundo número

        Returns:
            float: Resultado da soma
        """
        return float(a) + float(b)

    @staticmethod
    def math_subtract(a: Union[int, float], b: Union[int, float]) -> float:
        """Subtrai dois números."""
        return float(a) - float(b)

    @staticmethod
    def math_multiply(a: Union[int, float], b: Union[int, float]) -> float:
        """Multiplica dois números."""
        return float(a) * float(b)

    @staticmethod
    def math_divide(a: Union[int, float], b: Union[int, float]) -> float:
        """
        Divide dois números.

        Raises:
            ValueError: Se o divisor for zero
        """
        b = float(b)
        if b == 0:
            raise ValueError("Divisão por zero não permitida")
        return float(a) / b

    @staticmethod
    def math_power(a: Union[int, float], b: Union[int, float]) -> float:
        """Eleva a à potência b."""
        return float(a) ** float(b)

    @staticmethod
    def math_sqrt(a: Union[int, float]) -> float:
        """
        Calcula a raiz quadrada.

        Raises:
            ValueError: Se o número for negativo
        """
        value = float(a)
        if value < 0:
            raise ValueError("Raiz quadrada de número negativo não permitida")
        return math.sqrt(value)

    @staticmethod
    def math_abs(a: Union[int, float]) -> float:
        """Retorna o valor absoluto."""
        return abs(float(a))

    @staticmethod
    def math_floor(a: Union[int, float]) -> int:
        """Arredonda para baixo (piso)."""
        return math.floor(float(a))

    @staticmethod
    def math_ceil(a: Union[int, float]) -> int:
        """Arredonda para cima (teto)."""
        return math.ceil(float(a))

    @staticmethod
    def math_round(a: Union[int, float], decimals: int = 0) -> float:
        """Arredonda para n casas decimais."""
        return round(float(a), int(decimals))

    @staticmethod
    def math_max(*args: Union[int, float]) -> float:
        """
        Retorna o maior valor entre os argumentos.

        Raises:
            ValueError: Se nenhum argumento for fornecido
        """
        if not args:
            raise ValueError("math.max requer pelo menos um argumento")
        return max(float(x) for x in args)

    @staticmethod
    def math_min(*args: Union[int, float]) -> float:
        """
        Retorna o menor valor entre os argumentos.

        Raises:
            ValueError: Se nenhum argumento for fornecido
        """
        if not args:
            raise ValueError("math.min requer pelo menos um argumento")
        return min(float(x) for x in args)

    @staticmethod
    def math_factorial(n: int) -> int:
        """
        Calcula o fatorial de um número.

        Raises:
            ValueError: Se o número for negativo
        """
        n = int(n)
        if n < 0:
            raise ValueError("Fatorial de número negativo não permitido")
        return math.factorial(n)

    @staticmethod
    def math_percentage(value: Union[int, float], total: Union[int, float]) -> float:
        """Calcula a porcentagem de value em relação a total."""
        return (float(value) / float(total)) * 100 if float(total) != 0 else 0

    @staticmethod
    def math_average(*args: Union[int, float]) -> float:
        """Calcula a média aritmética dos valores fornecidos."""
        if not args:
            return 0
        return sum(float(x) for x in args) / len(args)

    # ------------------------------------------------------------------------
    # CATEGORIA: STRINGS
    # ------------------------------------------------------------------------

    @staticmethod
    def string_upper(text: str) -> str:
        """Converte string para maiúsculas."""
        return str(text).upper()

    @staticmethod
    def string_lower(text: str) -> str:
        """Converte string para minúsculas."""
        return str(text).lower()

    @staticmethod
    def string_capitalize(text: str) -> str:
        """Capitaliza a primeira letra da string."""
        return str(text).capitalize()

    @staticmethod
    def string_title(text: str) -> str:
        """Converte para formato título (primeira letra de cada palavra maiúscula)."""
        return str(text).title()

    @staticmethod
    def string_reverse(text: str) -> str:
        """Inverte a string."""
        return str(text)[::-1]

    @staticmethod
    def string_length(text: str) -> int:
        """Retorna o comprimento da string."""
        return len(str(text))

    @staticmethod
    def string_trim(text: str) -> str:
        """Remove espaços em branco das extremidades."""
        return str(text).strip()

    @staticmethod
    def string_replace(text: str, old: str, new: str) -> str:
        """Substitui todas as ocorrências de old por new."""
        return str(text).replace(str(old), str(new))

    @staticmethod
    def string_split(text: str, separator: str = " ") -> List[str]:
        """Divide a string em uma lista usando o separador."""
        return str(text).split(str(separator))

    @staticmethod
    def string_join(items: List[str], separator: str = " ") -> str:
        """Junta uma lista de strings usando o separador."""
        return str(separator).join(str(item) for item in items)

    @staticmethod
    def string_contains(text: str, substring: str) -> bool:
        """Verifica se a string contém o substring."""
        return str(substring) in str(text)

    @staticmethod
    def string_starts_with(text: str, prefix: str) -> bool:
        """Verifica se a string começa com o prefixo."""
        return str(text).startswith(str(prefix))

    @staticmethod
    def string_ends_with(text: str, suffix: str) -> bool:
        """Verifica se a string termina com o sufixo."""
        return str(text).endswith(str(suffix))

    @staticmethod
    def string_find(text: str, substring: str) -> int:
        """
        Encontra a posição da primeira ocorrência do substring.

        Returns:
            int: Posição encontrada ou -1 se não encontrado
        """
        return str(text).find(str(substring))

    @staticmethod
    def string_slice(text: str, start: int, end: Optional[int] = None) -> str:
        """Fatiamento de string (slice)."""
        start = int(start)
        return str(text)[start:] if end is None else str(text)[start:int(end)]

    @staticmethod
    def string_append(text: str, suffix: str) -> str:
        """Concatena duas strings."""
        return str(text) + str(suffix)

    @staticmethod
    def string_count(text: str, substring: str) -> int:
        """Conta ocorrências do substring na string."""
        return str(text).count(str(substring))

    @staticmethod
    def string_pad_left(text: str, length: int, char: str = " ") -> str:
        """Preenche a string à esquerda até o comprimento especificado."""
        return str(text).rjust(int(length), str(char)[0] if char else " ")

    @staticmethod
    def string_pad_right(text: str, length: int, char: str = " ") -> str:
        """Preenche a string à direita até o comprimento especificado."""
        return str(text).ljust(int(length), str(char)[0] if char else " ")

    # ------------------------------------------------------------------------
    # CATEGORIA: LISTAS
    # ------------------------------------------------------------------------

    @staticmethod
    def list_create(*items: Any) -> List[Any]:
        """Cria uma lista com os itens fornecidos."""
        return list(items)

    @staticmethod
    def list_append(items: List[Any], item: Any) -> List[Any]:
        """Adiciona um item ao final da lista."""
        result = list(items)
        result.append(item)
        return result

    @staticmethod
    def list_prepend(items: List[Any], item: Any) -> List[Any]:
        """Adiciona um item no início da lista."""
        result = list(items)
        result.insert(0, item)
        return result

    @staticmethod
    def list_remove(items: List[Any], item: Any) -> List[Any]:
        """Remove a primeira ocorrência do item da lista."""
        result = list(items)
        try:
            result.remove(item)
        except ValueError:
            pass  # Ignora se o item não existe
        return result

    @staticmethod
    def list_remove_at(items: List[Any], index: int) -> List[Any]:
        """Remove o item na posição especificada."""
        result = list(items)
        try:
            del result[int(index)]
        except IndexError:
            pass
        return result

    @staticmethod
    def list_length(items: List[Any]) -> int:
        """Retorna o comprimento da lista."""
        return len(list(items))

    @staticmethod
    def list_get(items: List[Any], index: int) -> Any:
        """Retorna o item na posição especificada."""
        return list(items)[int(index)]

    @staticmethod
    def list_set(items: List[Any], index: int, value: Any) -> List[Any]:
        """Define o valor na posição especificada."""
        result = list(items)
        result[int(index)] = value
        return result

    @staticmethod
    def list_reverse(items: List[Any]) -> List[Any]:
        """Inverte a ordem da lista."""
        return list(reversed(list(items)))

    @staticmethod
    def list_sort(items: List[Any], reverse: bool = False) -> List[Any]:
        """Ordena a lista."""
        return sorted(list(items), key=lambda x: str(x), reverse=bool(reverse))

    @staticmethod
    def list_sort_numeric(items: List[Union[int, float]], reverse: bool = False) -> List[Union[int, float]]:
        """Ordena a lista numericamente."""
        try:
            return sorted([float(x) for x in items], reverse=bool(reverse))
        except (ValueError, TypeError):
            return list(items)

    @staticmethod
    def list_slice(items: List[Any], start: int, end: Optional[int] = None) -> List[Any]:
        """Fatiamento da lista."""
        items = list(items)
        start = int(start)
        return items[start:] if end is None else items[start:int(end)]

    @staticmethod
    def list_index(items: List[Any], value: Any) -> int:
        """
        Retorna o índice do valor na lista.

        Raises:
            ValueError: Se o valor não for encontrado
        """
        return list(items).index(value)

    @staticmethod
    def list_contains(items: List[Any], value: Any) -> bool:
        """Verifica se a lista contém o valor."""
        return value in list(items)

    @staticmethod
    def list_unique(items: List[Any]) -> List[Any]:
        """Remove duplicatas da lista mantendo a ordem."""
        result = []
        for item in list(items):
            if item not in result:
                result.append(item)
        return result

    @staticmethod
    def list_merge(list1: List[Any], list2: List[Any]) -> List[Any]:
        """Funde duas listas."""
        return list(list1) + list(list2)

    @staticmethod
    def list_filter(items: List[Any], condition: str) -> List[Any]:
        """
        Filtra a lista por uma condição simples.

        Exemplo: list_filter([1,2,3,4,5], ">3") -> [4,5]
        """
        items = list(items)
        result = []
        condition = condition.strip()

        if condition.startswith(">"):
            threshold = float(condition[1:].strip())
            return [x for x in items if isinstance(x, (int, float)) and float(x) > threshold]
        elif condition.startswith("<"):
            threshold = float(condition[1:].strip())
            return [x for x in items if isinstance(x, (int, float)) and float(x) < threshold]
        elif condition.startswith(">="):
            threshold = float(condition[2:].strip())
            return [x for x in items if isinstance(x, (int, float)) and float(x) >= threshold]
        elif condition.startswith("<="):
            threshold = float(condition[2:].strip())
            return [x for x in items if isinstance(x, (int, float)) and float(x) <= threshold]
        elif condition.startswith("=="):
            value = condition[2:].strip()
            return [x for x in items if str(x) == value]
        else:
            # Retorna itens que contenham a string
            return [x for x in items if condition.lower() in str(x).lower()]

    # ------------------------------------------------------------------------
    # CATEGORIA: JSON
    # ------------------------------------------------------------------------

    @staticmethod
    def json_parse(json_string: str) -> Dict[str, Any]:
        """
        Converte uma string JSON para um objeto Python.

        Raises:
            ValueError: Se o JSON for inválido
        """
        try:
            return json.loads(str(json_string))
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON inválido: {e}")

    @staticmethod
    def json_stringify(obj: Any) -> str:
        """Converte um objeto Python para string JSON."""
        return json.dumps(obj, ensure_ascii=False, indent=2)

    @staticmethod
    def json_get(obj: Dict[str, Any], key: str, default: Any = None) -> Any:
        """Obtém um valor de um objeto JSON pela chave."""
        return obj.get(key, default)

    @staticmethod
    def json_set(obj: Dict[str, Any], key: str, value: Any) -> Dict[str, Any]:
        """Define um valor em um objeto JSON."""
        result = dict(obj)
        result[key] = value
        return result

    # ------------------------------------------------------------------------
    # CATEGORIA: DATAS
    # ------------------------------------------------------------------------

    @staticmethod
    def date_now() -> str:
        """Retorna a data e hora atual no formato ISO."""
        return dt.datetime.now().isoformat()

    @staticmethod
    def date_timestamp() -> int:
        """Retorna o timestamp UNIX atual."""
        return int(time.time())

    @staticmethod
    def date_format(date_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        """Formata uma data conforme o formato especificado."""
        try:
            dt_obj = dt.datetime.fromisoformat(str(date_str))
            return dt_obj.strftime(str(format_str))
        except ValueError:
            # Tenta parsear formatos comuns
            for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d/%m/%Y", "%d/%m/%Y %H:%M:%S"]:
                try:
                    dt_obj = dt.datetime.strptime(str(date_str), fmt)
                    return dt_obj.strftime(str(format_str))
                except ValueError:
                    continue
            raise ValueError(f"Formato de data inválido: {date_str}")

    @staticmethod
    def date_add_days(date_str: str, days: int) -> str:
        """Adiciona dias a uma data."""
        dt_obj = dt.datetime.fromisoformat(str(date_str))
        return (dt_obj + dt.timedelta(days=int(days))).isoformat()

    @staticmethod
    def date_add_hours(date_str: str, hours: int) -> str:
        """Adiciona horas a uma data."""
        dt_obj = dt.datetime.fromisoformat(str(date_str))
        return (dt_obj + dt.timedelta(hours=int(hours))).isoformat()

    @staticmethod
    def date_diff_days(date1: str, date2: str) -> int:
        """Calcula a diferença em dias entre duas datas."""
        dt1 = dt.datetime.fromisoformat(str(date1))
        dt2 = dt.datetime.fromisoformat(str(date2))
        return abs((dt2 - dt1).days)

    @staticmethod
    def date_parse(date_str: str) -> str:
        """
        Tenta parsear uma data em diferentes formatos e retorna no formato ISO.
        """
        for fmt in [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
            "%d/%m/%Y %H:%M:%S",
            "%d/%m/%Y",
            "%m/%d/%Y",
            "%Y%m%d"
        ]:
            try:
                dt_obj = dt.datetime.strptime(str(date_str), fmt)
                return dt_obj.isoformat()
            except ValueError:
                continue
        raise ValueError(f"Não foi possível parsear a data: {date_str}")

    # ------------------------------------------------------------------------
    # CATEGORIA: HTTP
    # ------------------------------------------------------------------------

    @staticmethod
    def http_get(url: str, headers: Optional[Dict[str, str]] = None) -> str:
        """
        Realiza uma requisição HTTP GET.

        Args:
            url: URL para requisição
            headers: Cabeçalhos HTTP opcionais

        Returns:
            str: Conteúdo da resposta
        """
        headers = headers or {}
        response = requests.get(str(url), timeout=REQUEST_TIMEOUT, headers=headers)
        response.raise_for_status()
        return response.text

    @staticmethod
    def http_get_json(url: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Realiza uma requisição HTTP GET e retorna o JSON parseado."""
        response_text = RokoTools.http_get(url, headers)
        return json.loads(response_text)

    @staticmethod
    def http_post(url: str, data: Optional[Dict[str, Any]] = None,
                  headers: Optional[Dict[str, str]] = None) -> str:
        """
        Realiza uma requisição HTTP POST com dados JSON.

        Args:
            url: URL para requisição
            data: Dados a serem enviados (serão convertidos para JSON)
            headers: Cabeçalhos HTTP opcionais

        Returns:
            str: Conteúdo da resposta
        """
        headers = headers or {"Content-Type": "application/json"}
        response = requests.post(str(url), json=data, timeout=REQUEST_TIMEOUT, headers=headers)
        response.raise_for_status()
        return response.text

    @staticmethod
    def http_put(url: str, data: Optional[Dict[str, Any]] = None,
                 headers: Optional[Dict[str, str]] = None) -> str:
        """Realiza uma requisição HTTP PUT."""
        headers = headers or {"Content-Type": "application/json"}
        response = requests.put(str(url), json=data, timeout=REQUEST_TIMEOUT, headers=headers)
        response.raise_for_status()
        return response.text

    @staticmethod
    def http_delete(url: str, headers: Optional[Dict[str, str]] = None) -> str:
        """Realiza uma requisição HTTP DELETE."""
        headers = headers or {}
        response = requests.delete(str(url), timeout=REQUEST_TIMEOUT, headers=headers)
        response.raise_for_status()
        return response.text

    @staticmethod
    def http_status(url: str) -> int:
        """Verifica o status HTTP de uma URL."""
        try:
            response = requests.head(str(url), timeout=REQUEST_TIMEOUT)
            return response.status_code
        except requests.RequestException:
            return -1

    # ------------------------------------------------------------------------
    # CATEGORIA: CRIPTOGRAFIA
    # ------------------------------------------------------------------------

    @staticmethod
    def crypto_uuid() -> str:
        """Gera um UUID versão 4."""
        return str(uuid.uuid4())

    @staticmethod
    def crypto_hash(text: str) -> str:
        """Gera o hash SHA-256 do texto."""
        return hashlib.sha256(str(text).encode("utf-8")).hexdigest()

    @staticmethod
    def crypto_md5(text: str) -> str:
        """Gera o hash MD5 do texto."""
        return hashlib.md5(str(text).encode("utf-8")).hexdigest()

    @staticmethod
    def crypto_sha1(text: str) -> str:
        """Gera o hash SHA-1 do texto."""
        return hashlib.sha1(str(text).encode("utf-8")).hexdigest()

    @staticmethod
    def crypto_random_string(length: int = 16) -> str:
        """Gera uma string aleatória de comprimento especificado."""
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        return "".join(random.choice(chars) for _ in range(int(length)))

    # ------------------------------------------------------------------------
    # CATEGORIA: ALEATÓRIO
    # ------------------------------------------------------------------------

    @staticmethod
    def random_number(min_val: int, max_val: int) -> int:
        """Gera um número inteiro aleatório entre min e max (inclusive)."""
        return random.randint(int(min_val), int(max_val))

    @staticmethod
    def random_float(min_val: float, max_val: float) -> float:
        """Gera um número decimal aleatório entre min e max."""
        return random.uniform(float(min_val), float(max_val))

    @staticmethod
    def random_choice(items: List[Any]) -> Any:
        """
        Escolhe um item aleatório da lista.

        Raises:
            ValueError: Se a lista estiver vazia
        """
        items = list(items)
        if not items:
            raise ValueError("random.choice requer uma lista não vazia")
        return random.choice(items)

    @staticmethod
    def random_shuffle(items: List[Any]) -> List[Any]:
        """Embaralha a lista aleatoriamente."""
        result = list(items)
        random.shuffle(result)
        return result

    @staticmethod
    def random_boolean() -> bool:
        """Retorna True ou False aleatoriamente."""
        return random.choice([True, False])

    # ------------------------------------------------------------------------
    # CATEGORIA: LOG
    # ------------------------------------------------------------------------

    @staticmethod
    def log_print(message: str, level: str = "INFO") -> str:
        """
        Registra uma mensagem no log.

        Args:
            message: Mensagem a ser registrada
            level: Nível do log (INFO, DEBUG, WARNING, ERROR)

        Returns:
            str: Mensagem registrada
        """
        timestamp = dt.datetime.now().isoformat()
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry, file=sys.stdout)

        # Salva em arquivo de log
        try:
            log_file = LOGS_FOLDER / f"roko_{dt.datetime.now().strftime('%Y-%m-%d')}.log"
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(log_entry + "\n")
        except OSError:
            pass  # Ignora erro de escrita em arquivo

        return f"Logged: {message}"

    @staticmethod
    def log_debug(message: str) -> str:
        """Registra uma mensagem de debug."""
        return RokoTools.log_print(message, "DEBUG")

    @staticmethod
    def log_warning(message: str) -> str:
        """Registra uma mensagem de aviso."""
        return RokoTools.log_print(message, "WARNING")

    @staticmethod
    def log_error(message: str) -> str:
        """Registra uma mensagem de erro."""
        return RokoTools.log_print(message, "ERROR")

    # ------------------------------------------------------------------------
    # CATEGORIA: SISTEMA
    # ------------------------------------------------------------------------

    @staticmethod
    def system_env(key: str) -> Optional[str]:
        """Retorna o valor de uma variável de ambiente."""
        return os.environ.get(str(key))

    @staticmethod
    def system_version() -> str:
        """Retorna a versão do sistema."""
        return TOOL_VERSION

    @staticmethod
    def system_time() -> str:
        """Retorna a hora atual formatada."""
        return dt.datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def system_date() -> str:
        """Retorna a data atual formatada."""
        return dt.datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def system_platform() -> str:
        """Retorna informações da plataforma."""
        return f"{sys.platform} - Python {sys.version}"


# ============================================================================
# ESPECIFICAÇÕES DAS FERRAMENTAS
# ============================================================================

TOOL_SPECS: Dict[str, Dict[str, Any]] = {
    # Matemática
    "math.sum": {"fn": RokoTools.math_sum, "category": "math",
                 "description": "Soma dois números", "parameters": ["a", "b"]},
    "math.subtract": {"fn": RokoTools.math_subtract, "category": "math",
                      "description": "Subtrai dois números", "parameters": ["a", "b"]},
    "math.multiply": {"fn": RokoTools.math_multiply, "category": "math",
                      "description": "Multiplica dois números", "parameters": ["a", "b"]},
    "math.divide": {"fn": RokoTools.math_divide, "category": "math",
                    "description": "Divide dois números", "parameters": ["a", "b"]},
    "math.power": {"fn": RokoTools.math_power, "category": "math",
                   "description": "Eleva à potência", "parameters": ["a", "b"]},
    "math.sqrt": {"fn": RokoTools.math_sqrt, "category": "math",
                  "description": "Raiz quadrada", "parameters": ["a"]},
    "math.abs": {"fn": RokoTools.math_abs, "category": "math",
                 "description": "Valor absoluto", "parameters": ["a"]},
    "math.floor": {"fn": RokoTools.math_floor, "category": "math",
                   "description": "Arredonda para baixo", "parameters": ["a"]},
    "math.ceil": {"fn": RokoTools.math_ceil, "category": "math",
                  "description": "Arredonda para cima", "parameters": ["a"]},
    "math.round": {"fn": RokoTools.math_round, "category": "math",
                   "description": "Arredonda para n casas decimais", "parameters": ["a", "decimals"]},
    "math.max": {"fn": RokoTools.math_max, "category": "math",
                 "description": "Retorna o maior valor", "parameters": ["args..."]},
    "math.min": {"fn": RokoTools.math_min, "category": "math",
                 "description": "Retorna o menor valor", "parameters": ["args..."]},
    "math.factorial": {"fn": RokoTools.math_factorial, "category": "math",
                       "description": "Fatorial de um número", "parameters": ["n"]},
    "math.percentage": {"fn": RokoTools.math_percentage, "category": "math",
                        "description": "Calcula a porcentagem", "parameters": ["value", "total"]},
    "math.average": {"fn": RokoTools.math_average, "category": "math",
                     "description": "Calcula a média aritmética", "parameters": ["args..."]},

    # Strings
    "string.upper": {"fn": RokoTools.string_upper, "category": "string",
                     "description": "Converte para maiúsculas", "parameters": ["text"]},
    "string.lower": {"fn": RokoTools.string_lower, "category": "string",
                     "description": "Converte para minúsculas", "parameters": ["text"]},
    "string.capitalize": {"fn": RokoTools.string_capitalize, "category": "string",
                          "description": "Capitaliza a string", "parameters": ["text"]},
    "string.title": {"fn": RokoTools.string_title, "category": "string",
                     "description": "Converte para formato título", "parameters": ["text"]},
    "string.reverse": {"fn": RokoTools.string_reverse, "category": "string",
                       "description": "Inverte a string", "parameters": ["text"]},
    "string.length": {"fn": RokoTools.string_length, "category": "string",
                      "description": "Tamanho da string", "parameters": ["text"]},
    "string.trim": {"fn": RokoTools.string_trim, "category": "string",
                    "description": "Remove espaços em branco", "parameters": ["text"]},
    "string.replace": {"fn": RokoTools.string_replace, "category": "string",
                       "description": "Substitui texto", "parameters": ["text", "old", "new"]},
    "string.split": {"fn": RokoTools.string_split, "category": "string",
                     "description": "Divide string em lista", "parameters": ["text", "separator"]},
    "string.join": {"fn": RokoTools.string_join, "category": "string",
                    "description": "Junta lista em string", "parameters": ["items", "separator"]},
    "string.contains": {"fn": RokoTools.string_contains, "category": "string",
                        "description": "Verifica se contém substring", "parameters": ["text", "substring"]},
    "string.starts_with": {"fn": RokoTools.string_starts_with, "category": "string",
                           "description": "Verifica prefixo", "parameters": ["text", "prefix"]},
    "string.ends_with": {"fn": RokoTools.string_ends_with, "category": "string",
                         "description": "Verifica sufixo", "parameters": ["text", "suffix"]},
    "string.find": {"fn": RokoTools.string_find, "category": "string",
                    "description": "Encontra posição da substring", "parameters": ["text", "substring"]},
    "string.slice": {"fn": RokoTools.string_slice, "category": "string",
                     "description": "Fatiamento de string", "parameters": ["text", "start", "end"]},
    "string.append": {"fn": RokoTools.string_append, "category": "string",
                      "description": "Concatena strings", "parameters": ["text", "suffix"]},
    "string.count": {"fn": RokoTools.string_count, "category": "string",
                     "description": "Conta ocorrências", "parameters": ["text", "substring"]},
    "string.pad_left": {"fn": RokoTools.string_pad_left, "category": "string",
                        "description": "Preenche à esquerda", "parameters": ["text", "length", "char"]},
    "string.pad_right": {"fn": RokoTools.string_pad_right, "category": "string",
                         "description": "Preenche à direita", "parameters": ["text", "length", "char"]},

    # Listas
    "list.create": {"fn": RokoTools.list_create, "category": "list",
                    "description": "Cria uma lista", "parameters": ["items..."]},
    "list.append": {"fn": RokoTools.list_append, "category": "list",
                    "description": "Adiciona item ao final", "parameters": ["items", "item"]},
    "list.prepend": {"fn": RokoTools.list_prepend, "category": "list",
                     "description": "Adiciona item no início", "parameters": ["items", "item"]},
    "list.remove": {"fn": RokoTools.list_remove, "category": "list",
                    "description": "Remove item da lista", "parameters": ["items", "item"]},
    "list.remove_at": {"fn": RokoTools.list_remove_at, "category": "list",
                       "description": "Remove item por índice", "parameters": ["items", "index"]},
    "list.length": {"fn": RokoTools.list_length, "category": "list",
                    "description": "Tamanho da lista", "parameters": ["items"]},
    "list.get": {"fn": RokoTools.list_get, "category": "list",
                 "description": "Obtém item por índice", "parameters": ["items", "index"]},
    "list.set": {"fn": RokoTools.list_set, "category": "list",
                 "description": "Define item por índice", "parameters": ["items", "index", "value"]},
    "list.reverse": {"fn": RokoTools.list_reverse, "category": "list",
                     "description": "Inverte a lista", "parameters": ["items"]},
    "list.sort": {"fn": RokoTools.list_sort, "category": "list",
                  "description": "Ordena a lista", "parameters": ["items", "reverse"]},
    "list.sort_numeric": {"fn": RokoTools.list_sort_numeric, "category": "list",
                          "description": "Ordena numericamente", "parameters": ["items", "reverse"]},
    "list.slice": {"fn": RokoTools.list_slice, "category": "list",
                   "description": "Fatiamento de lista", "parameters": ["items", "start", "end"]},
    "list.index": {"fn": RokoTools.list_index, "category": "list",
                   "description": "Índice do item", "parameters": ["items", "value"]},
    "list.contains": {"fn": RokoTools.list_contains, "category": "list",
                      "description": "Verifica se contém item", "parameters": ["items", "value"]},
    "list.unique": {"fn": RokoTools.list_unique, "category": "list",
                    "description": "Remove duplicatas", "parameters": ["items"]},
    "list.merge": {"fn": RokoTools.list_merge, "category": "list",
                   "description": "Funde duas listas", "parameters": ["list1", "list2"]},
    "list.filter": {"fn": RokoTools.list_filter, "category": "list",
                    "description": "Filtra a lista", "parameters": ["items", "condition"]},

    # JSON
    "json.parse": {"fn": RokoTools.json_parse, "category": "json",
                   "description": "Converte JSON para objeto", "parameters": ["json_string"]},
    "json.stringify": {"fn": RokoTools.json_stringify, "category": "json",
                       "description": "Converte objeto para JSON", "parameters": ["obj"]},
    "json.get": {"fn": RokoTools.json_get, "category": "json",
                 "description": "Obtém valor por chave", "parameters": ["obj", "key", "default"]},
    "json.set": {"fn": RokoTools.json_set, "category": "json",
                 "description": "Define valor por chave", "parameters": ["obj", "key", "value"]},

    # Datas
    "date.now": {"fn": RokoTools.date_now, "category": "date",
                 "description": "Data e hora atual", "parameters": []},
    "date.timestamp": {"fn": RokoTools.date_timestamp, "category": "date",
                       "description": "Timestamp atual", "parameters": []},
    "date.format": {"fn": RokoTools.date_format, "category": "date",
                    "description": "Formata data", "parameters": ["date_str", "format_str"]},
    "date.add_days": {"fn": RokoTools.date_add_days, "category": "date",
                      "description": "Adiciona dias a uma data", "parameters": ["date_str", "days"]},
    "date.add_hours": {"fn": RokoTools.date_add_hours, "category": "date",
                       "description": "Adiciona horas a uma data", "parameters": ["date_str", "hours"]},
    "date.diff_days": {"fn": RokoTools.date_diff_days, "category": "date",
                       "description": "Diferença em dias entre duas datas", "parameters": ["date1", "date2"]},
    "date.parse": {"fn": RokoTools.date_parse, "category": "date",
                   "description": "Parseia data em múltiplos formatos", "parameters": ["date_str"]},

    # HTTP
    "http.get": {"fn": RokoTools.http_get, "category": "http",
                 "description": "Requisição HTTP GET", "parameters": ["url", "headers"]},
    "http.get_json": {"fn": RokoTools.http_get_json, "category": "http",
                      "description": "HTTP GET com retorno JSON", "parameters": ["url", "headers"]},
    "http.post": {"fn": RokoTools.http_post, "category": "http",
                  "description": "Requisição HTTP POST", "parameters": ["url", "data", "headers"]},
    "http.put": {"fn": RokoTools.http_put, "category": "http",
                 "description": "Requisição HTTP PUT", "parameters": ["url", "data", "headers"]},
    "http.delete": {"fn": RokoTools.http_delete, "category": "http",
                    "description": "Requisição HTTP DELETE", "parameters": ["url", "headers"]},
    "http.status": {"fn": RokoTools.http_status, "category": "http",
                    "description": "Verifica status HTTP", "parameters": ["url"]},

    # Criptografia
    "crypto.uuid": {"fn": RokoTools.crypto_uuid, "category": "crypto",
                    "description": "Gera UUID", "parameters": []},
    "crypto.hash": {"fn": RokoTools.crypto_hash, "category": "crypto",
                    "description": "Gera hash SHA-256", "parameters": ["text"]},
    "crypto.md5": {"fn": RokoTools.crypto_md5, "category": "crypto",
                   "description": "Gera hash MD5", "parameters": ["text"]},
    "crypto.sha1": {"fn": RokoTools.crypto_sha1, "category": "crypto",
                    "description": "Gera hash SHA-1", "parameters": ["text"]},
    "crypto.random_string": {"fn": RokoTools.crypto_random_string, "category": "crypto",
                             "description": "Gera string aleatória", "parameters": ["length"]},

    # Aleatório
    "random.number": {"fn": RokoTools.random_number, "category": "random",
                      "description": "Número inteiro aleatório", "parameters": ["min_val", "max_val"]},
    "random.float": {"fn": RokoTools.random_float, "category": "random",
                     "description": "Número decimal aleatório", "parameters": ["min_val", "max_val"]},
    "random.choice": {"fn": RokoTools.random_choice, "category": "random",
                      "description": "Escolhe item aleatório", "parameters": ["items"]},
    "random.shuffle": {"fn": RokoTools.random_shuffle, "category": "random",
                       "description": "Embaralha lista", "parameters": ["items"]},
    "random.boolean": {"fn": RokoTools.random_boolean, "category": "random",
                       "description": "Valor booleano aleatório", "parameters": []},

    # Log
    "log.print": {"fn": RokoTools.log_print, "category": "log",
                  "description": "Registra log INFO", "parameters": ["message", "level"]},
    "log.debug": {"fn": RokoTools.log_debug, "category": "log",
                  "description": "Registra log DEBUG", "parameters": ["message"]},
    "log.warning": {"fn": RokoTools.log_warning, "category": "log",
                    "description": "Registra log WARNING", "parameters": ["message"]},
    "log.error": {"fn": RokoTools.log_error, "category": "log",
                  "description": "Registra log ERROR", "parameters": ["message"]},

    # Sistema
    "system.env": {"fn": RokoTools.system_env, "category": "system",
                   "description": "Variável de ambiente", "parameters": ["key"]},
    "system.version": {"fn": RokoTools.system_version, "category": "system",
                       "description": "Versão do sistema", "parameters": []},
    "system.time": {"fn": RokoTools.system_time, "category": "system",
                    "description": "Hora atual", "parameters": []},
    "system.date": {"fn": RokoTools.system_date, "category": "system",
                    "description": "Data atual", "parameters": []},
    "system.platform": {"fn": RokoTools.system_platform, "category": "system",
                        "description": "Informações da plataforma", "parameters": []},
}


# ============================================================================
# FERRAMENTAS META (METADADOS)
# ============================================================================

def meta_categories() -> Dict[str, List[str]]:
    """
    Retorna todas as categorias de ferramentas com suas respectivas ferramentas.

    Returns:
        Dict[str, List[str]]: Dicionário com categorias e listas de ferramentas
    """
    categories: Dict[str, List[str]] = {}
    for name, spec in TOOL_SPECS.items():
        categories.setdefault(spec["category"], []).append(name)

    # Adiciona a categoria meta
    categories["meta"] = ["meta.tools", "meta.categories", "meta.help", "meta.info", "meta.search"]

    # Ordena tudo
    for names in categories.values():
        names.sort()
    return dict(sorted(categories.items()))


def meta_tools() -> Dict[str, Dict[str, Any]]:
    """
    Retorna todas as ferramentas disponíveis com suas especificações.

    Returns:
        Dict[str, Dict[str, Any]]: Dicionário com todas as ferramentas
    """
    tools = {
        name: {
            "category": spec["category"],
            "description": spec["description"],
            "parameters": list(spec.get("parameters", [])),
        }
        for name, spec in TOOL_SPECS.items()
    }

    # Adiciona as ferramentas meta
    tools.update({
        "meta.tools": {"category": "meta", "description": "Lista todas as ferramentas", "parameters": []},
        "meta.categories": {"category": "meta", "description": "Lista todas as categorias", "parameters": []},
        "meta.help": {"category": "meta", "description": "Ajuda sobre uma ferramenta", "parameters": ["tool_name"]},
        "meta.info": {"category": "meta", "description": "Informações do sistema", "parameters": []},
        "meta.search": {"category": "meta", "description": "Busca ferramentas por termo", "parameters": ["query"]},
    })

    return dict(sorted(tools.items()))


def meta_help(tool_name: str) -> Dict[str, Any]:
    """
    Retorna informações detalhadas sobre uma ferramenta específica.

    Args:
        tool_name: Nome da ferramenta

    Returns:
        Dict[str, Any]: Informações da ferramenta
    """
    if tool_name in TOOL_SPECS:
        spec = TOOL_SPECS[tool_name]
        return {
            "name": tool_name,
            "category": spec["category"],
            "description": spec["description"],
            "parameters": spec.get("parameters", []),
            "available": True
        }

    # Meta tools
    meta_tool_info = {
        "meta.tools": {"category": "meta", "description": "Lista todas as ferramentas", "parameters": []},
        "meta.categories": {"category": "meta", "description": "Lista todas as categorias", "parameters": []},
        "meta.help": {"category": "meta", "description": "Ajuda sobre uma ferramenta", "parameters": ["tool_name"]},
        "meta.info": {"category": "meta", "description": "Informações do sistema", "parameters": []},
        "meta.search": {"category": "meta", "description": "Busca ferramentas por termo", "parameters": ["query"]},
    }

    if tool_name in meta_tool_info:
        info = meta_tool_info[tool_name]
        return {
            "name": tool_name,
            "category": info["category"],
            "description": info["description"],
            "parameters": info["parameters"],
            "available": True
        }

    return {"name": tool_name, "available": False, "error": f"Ferramenta '{tool_name}' não encontrada"}


def meta_info() -> Dict[str, Any]:
    """
    Retorna informações gerais sobre o sistema.

    Returns:
        Dict[str, Any]: Informações do sistema
    """
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "api_version": API_VERSION,
        "tool_version": TOOL_VERSION,
        "total_tools": len(TOOL_SPECS) + 5,  # +5 ferramentas meta
        "categories": len(meta_categories()),
        "description": "API de automação e execução de ferramentas",
        "status": "online",
        "timestamp": dt.datetime.now().isoformat(),
    }


def _fold_accents(text: str) -> str:
    """
    Remove acentos/diacríticos de um texto (á->a, número->numero, ção->cao),
    preservando o restante. Usado por meta_search() para que buscas em
    português funcionem independente de o termo digitado ter acento ou não
    — sem isso, "numero" nunca bateria com "número" numa comparação de
    substring simples, o que prejudicava bastante a precisão de qualquer
    busca/roteamento por palavra-chave em português (ex.: o router
    semântico ROKO_ROUTER.hmp depende diretamente disso).
    """
    normalized = unicodedata.normalize("NFD", text)
    return "".join(c for c in normalized if unicodedata.category(c) != "Mn")


def meta_search(query: str) -> List[Dict[str, Any]]:
    """
    Busca ferramentas por termo (tolerante a acentuação: "numero" encontra
    "número", "servico" encontra "serviço", etc).

    Args:
        query: Termo de busca

    Returns:
        List[Dict[str, Any]]: Lista de ferramentas encontradas
    """
    query = _fold_accents(query.lower().strip())
    results = []

    for name, spec in TOOL_SPECS.items():
        if (query in _fold_accents(name.lower()) or
            query in _fold_accents(spec["category"].lower()) or
            query in _fold_accents(spec["description"].lower()) or
            any(query in _fold_accents(p.lower()) for p in spec.get("parameters", []))):
            results.append({
                "name": name,
                "category": spec["category"],
                "description": spec["description"],
                "parameters": spec.get("parameters", [])
            })

    return sorted(results, key=lambda x: x["name"])


# ============================================================================
# EXECUTOR DE FERRAMENTAS
# ============================================================================

def execute_tool(tool_name: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Executa uma ferramenta com os parâmetros fornecidos.

    Args:
        tool_name: Nome da ferramenta a ser executada
        params: Parâmetros para a ferramenta

    Returns:
        Dict[str, Any]: Resultado da execução com status de sucesso
    """
    params = params or {}

    # Ferramentas meta
    if tool_name == "meta.tools":
        return {"success": True, "result": meta_tools()}
    if tool_name == "meta.categories":
        return {"success": True, "result": meta_categories()}
    if tool_name == "meta.help":
        return {"success": True, "result": meta_help(params.get("tool_name", ""))}
    if tool_name == "meta.info":
        return {"success": True, "result": meta_info()}
    if tool_name == "meta.search":
        return {"success": True, "result": meta_search(params.get("query", ""))}

    # Ferramentas padrão
    spec = TOOL_SPECS.get(tool_name)
    if spec is None:
        return {"success": False, "error": f"Ferramenta '{tool_name}' não encontrada"}

    fn = spec["fn"]

    try:
        if _accepts_var_positional(fn):
            # Ferramentas declaradas com *args (ex.: math.max, math.min,
            # math.average, list.create) não podem ser chamadas com
            # fn(**params) — *args não aceita argumentos nomeados. Isso
            # as deixava permanentemente quebradas via CALL/execute_tool
            # (erro "got an unexpected keyword argument"), mesmo estando
            # documentadas e listadas em /tools. Resolvido convertendo os
            # parâmetros para posicionais:
            #   - Se vier um único parâmetro cujo valor é lista/tupla
            #     (ex.: WITH items=[1,2,3]), os itens são espalhados.
            #   - Caso contrário, os valores dos parâmetros são passados
            #     na ordem em que foram informados na chamada
            #     (ex.: WITH a=1, b=5, c=3 -> fn(1, 5, 3)).
            values = list(params.values())
            if len(values) == 1 and isinstance(values[0], (list, tuple)):
                args = list(values[0])
            else:
                args = values
            result = fn(*args)
        else:
            result = fn(**params)
        return {"success": True, "result": result}
    except TypeError as e:
        return {"success": False, "error": f"Erro de parâmetros: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def _accepts_var_positional(fn: Callable) -> bool:
    """Indica se `fn` declara um parâmetro *args (VAR_POSITIONAL)."""
    try:
        sig = inspect.signature(fn)
    except (TypeError, ValueError):
        return False
    return any(p.kind == inspect.Parameter.VAR_POSITIONAL for p in sig.parameters.values())
