# -*- coding: utf-8 -*-
"""Used to record prompts, will be replaced by configuration"""
from agentscope.parsers import MarkdownJsonDictParser


class Prompts:
    """Prompts for game LLM"""

    to_attackers = (
        "{0}, you are the attackers. \nThe defenders' positions are:\n{1} "
        "And your positions are:\n{2}"
        "Discuss with your teammates, come up with a strategy about how to  get into the win-area to win the game, "
        "and decide on your own distance and direction.\n"
        "You must provide your own distance and direction in the form of (radius, angle). radius is between 0 and 1, "
        "angle is between 0 and 2*pi."
    )

    to_attackers_chinese = (
        "{0}, 你们是进攻方。进攻方的位置是：\n{1} "
        "你们的位置是：\n{2}"
        "与队友讨论，制定策略，决定如何进入胜利区域赢得比赛，并决定自己的距离和方向。\n"
        "你必须提供自己的距离和方向，形式为（半径，角度）。半径在0到1之间，角度在0到2*pi之间。"
    )

    to_defenders = (
        "{0}, you are the defenders. The attackers' positions are:\n{1} "
        "and your positions are:\n{2}"
        "Discuss with your teammates, come up with a strategy, and decide on your own distance and direction.\n"
        "You must provide your own distance and direction in the form of (radius, angle). radius is between 0 and 1, "
        "angle is between 0 and 2*pi."
    )

    to_defenders_chinese = (
        "{0}, 你们是防守方。进攻方的位置是：\n{1} "
        "你们的位置是：\n{2}"
        "与队友讨论，制定策略，决定自己的距离和方向。\n"
        "你必须提供自己的距离和方向，形式为（半径，角度）。半径在0到1之间，角度在0到2*pi之间。"
    )

    usv_discuss_parser = MarkdownJsonDictParser(
        content_hint={
            "thought": "what you thought",
            "speak": "what you speak",
            "finish_discussion": "whether the discussion reached an "
            "agreement or not (true/false)",
        },
        required_keys=["thought", "speak", "finish_discussion"],
        keys_to_memory="speak",
        keys_to_content="speak",
        keys_to_metadata=["finish_discussion"],
    )

    usv_discuss_parser_chinese = MarkdownJsonDictParser(
        content_hint={
            "thought": "你的想法",
            "speak": "你说的话",
            "finish_discussion": "讨论是否达成一致（true/false）",
        },
        required_keys=["thought", "speak", "finish_discussion"],
        keys_to_memory="speak",
        keys_to_content="speak",
        keys_to_metadata=["finish_discussion"],
    )

    to_usvs_move = "Where do you want to go? Give me (radius, angle)."

    to_usvs_move_chinese = "你要向哪里移动？"

    to_usv_invalid_move = ("You give an invalid move into defenders' defend area, please try again. What's your move "
                           "distance and angle?")

    to_usv_invalid_move_chinese = "你给出了一个无效的移动到防守区域的移动，请重试。你的移动距离和角度是多少？"

    usv_move_parser = MarkdownJsonDictParser(
        content_hint={
            "speak": "where you want to move",
            "direction": "the direction you want to move（a float between 0 and 2*pi）",
            "distance": "the distance you want to move（a float between 0 and 1）",
        },
        required_keys=["speak", "direction", "distance"],
        keys_to_memory="speak",
        keys_to_content="speak",
        keys_to_metadata=["direction", "distance"],
    )

    usv_move_parser_chinese = MarkdownJsonDictParser(
        content_hint={
            "speak": "你想移动到哪里?",
            "direction": "你想移动的方向（0到2*pi之间的浮点数）",
            "distance": "你想移动的距离（0到1之间的浮点数）",
        },
        required_keys=["speak", "direction", "distance"],
        keys_to_memory="speak",
        keys_to_content="speak",
        keys_to_metadata=["direction", "distance"],
    )