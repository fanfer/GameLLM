# -*- coding: utf-8 -*-
"""utils."""
import math
import re
from typing import Union, Any, Sequence

import numpy as np
from loguru import logger

from USV import USV
from prompt import Prompts
from agentscope.agents import AgentBase
from agentscope.message import Msg


def check_winning(attackers) -> bool:
    """check which group wins"""
    for attacker in attackers:
        if attacker.x ** 2 + attacker.y ** 2 < 25:
            return True
    return False


def parse_value(value_str):
    # 替换 'pi' 为 math.pi
    value_str = value_str.replace('pi', f'{math.pi}')

    # 计算表达式的值
    return eval(value_str)


def extract_first_parentheses(text):
    # 使用正则表达式匹配第一个括号及其内容
    match = re.search(r'\(([^)]*)\)', text)
    if match:
        # 返回括号中的内容
        return match.group(1)
    else:
        numbers = re.findall(r'-?\d+\.?\d*', text)
        if len(numbers) >= 2:
            distance = float(numbers[0])
            direction = float(numbers[1])
            return f"({distance}, {direction})"


def extract_distance_and_direction(generate) -> tuple[float, float]:
    """extract player direction and id distance a string"""
    numbers_str = [generate.metadata["distance"], generate.metadata["direction"]]
    if type(numbers_str[1]) != str:
        # distance = parse_value(numbers_str[0])
        # direction = parse_value(numbers_str[1])
        direction = float(numbers_str[1])
    else:
        direction = parse_value(numbers_str[1])
    distance = float(numbers_str[0])

    return distance, direction


def n2s(agents: Sequence[Union[AgentBase, str]]) -> str:
    """combine agent names into a string, and use "and" to connect the last
    two names."""

    def _get_name(agent_: Union[AgentBase, str]) -> str:
        return agent_.name if isinstance(agent_, AgentBase) else agent_

    if len(agents) == 1:
        return _get_name(agents[0])

    return (
            ", ".join([_get_name(_) for _ in agents[:-1]])
            + " and "
            + _get_name(agents[-1])
    )


def agents_positions(agents: Sequence[USV]) -> str:
    """get agents' positions"""
    return (
            ", ".join([f"{agent.name}: ({agent.x}, {agent.y})" for agent in agents[:-1]])
            + " and "
            + f"{agents[-1].name}: ({agents[-1].x}, {agents[-1].y})\n"
    )


def set_parsers(
        agents: Union[AgentBase, list[AgentBase]],
        parser_name: str,
) -> None:
    """Add parser to agents"""
    if not isinstance(agents, list):
        agents = [agents]
    for agent in agents:
        agent.set_parser(parser_name)
