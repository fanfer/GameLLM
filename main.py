# 这是一个示例 Python 脚本。
import math
from datetime import datetime
from functools import partial

import agentscope
import numpy as np
from agentscope import msghub
from agentscope.message import Msg
from agentscope.pipelines import sequentialpipeline

from USV import USV
from game_utils import n2s, set_parsers, agents_positions, extract_distance_and_direction, check_winning
from prompt import Prompts

# 按 ⌃R 执行或将其替换为您的代码。
# 按 双击 ⇧ 在所有地方搜索类、文件、工具窗口、操作和设置。
USV_COUNTS = 6
ATTACKER_COUNTS = 3


def main() -> None:
    """Game LLM main function."""
    HostMsg = partial(Msg, name="Moderator", role="assistant", echo=True)
    MAX_PLAYER_DISCUSSION_ROUND = 3
    MAX_GAME_ROUND = 10
    players = agentscope.init(
        model_configs="./configs/model_configs.json",
        agent_configs="./configs/agent_configs.json",
        logger_level="DEBUG"
    )

    roles = ["attacker", "attacker", "attacker", "defender", "defender", "defender"]
    attackers = players[:ATTACKER_COUNTS]
    defenders = players[ATTACKER_COUNTS:-2]
    attacker_with_Master = [players[-2]] + attackers
    defender_with_Master = [players[-1]] + defenders

    random_numbers = np.random.uniform(0, np.pi, 3)
    random_numbers_2 = np.random.uniform(0, np.pi, 3)

    for i in range(USV_COUNTS):
        if i < ATTACKER_COUNTS:
            usv = USV(name=f"Player{i + 1}", role=roles[i], x=10 * math.sin(random_numbers[i]),
                      y=10 * math.cos(random_numbers[i]), agent=players[i])
        else:
            usv = USV(name=f"Player{i + 1}", role=roles[i], x=6 * math.sin(random_numbers_2[i - 3]),
                      y=6 * math.cos(random_numbers_2[i - 3]), agent=players[i])
        USV.usvs.append(usv)
    attacker_usvs = USV.usvs[:ATTACKER_COUNTS]
    defender_usvs = USV.usvs[ATTACKER_COUNTS:]

    # 获取当前时间戳
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    # 构造文件名
    filename = f"txt_gif/file-{timestamp}.txt"

    for frame in range(1, MAX_GAME_ROUND + 1):
        # attackers discuss
        hint = HostMsg(content=Prompts.to_attackers.format(n2s(attacker_with_Master), agents_positions(USV.usvs[ATTACKER_COUNTS:]),
                                                           agents_positions(USV.usvs[:ATTACKER_COUNTS])))
        with msghub(attacker_with_Master, hint) as hub:
            set_parsers(attacker_with_Master, Prompts.usv_discuss_parser)
            for _ in range(MAX_PLAYER_DISCUSSION_ROUND):
                x = sequentialpipeline(attacker_with_Master)
                if x.metadata.get("finish_discussion", False):
                    break
            set_parsers(attackers, Prompts.usv_move_parser)
            hint = HostMsg(content=Prompts.to_usvs_move)
            for attacker in attacker_usvs:
                max_round = 0
                agent = attacker.agent
                generate_moving = agent(hint)
                distance, direction= extract_distance_and_direction(generate_moving)

                while not attacker.move(distance, direction):
                    max_round += 1
                    if max_round > 4:
                        defender.move(0, 0)
                        break
                    x = agent(HostMsg(content=Prompts.to_usv_invalid_move))
                    distance, direction = extract_distance_and_direction(x)

        # defenders discuss
        hint = HostMsg(content=Prompts.to_defenders.format(n2s(defender_with_Master), agents_positions(USV.usvs[:ATTACKER_COUNTS]),
                                                           agents_positions(USV.usvs[ATTACKER_COUNTS:])))
        with msghub(defender_with_Master, hint) as hub:
            set_parsers(defender_with_Master, Prompts.usv_discuss_parser)
            for _ in range(MAX_PLAYER_DISCUSSION_ROUND):
                x = sequentialpipeline(defender_with_Master)
                if x.metadata.get("finish_discussion", False):
                    break
            set_parsers(defenders, Prompts.usv_move_parser)
            hint = HostMsg(content=Prompts.to_usvs_move)
            for defender in defender_usvs:
                max_round = 0
                agent = defender.agent
                generate_moving = agent(hint)
                distance, direction = extract_distance_and_direction(generate_moving)
                while not defender.move(distance, direction):
                    max_round += 1
                    if max_round > 4:
                        defender.move(0, 0)
                        break
                    x = agent(HostMsg(content=Prompts.to_usv_invalid_move))
                    distance, direction = extract_distance_and_direction(x)

        with open(filename, 'a') as f:
            f.write(f"Round {frame}:")
            for usv in USV.usvs:
                f.write(f"{usv.name}: ({usv.x}, {usv.y});")
            f.write("\n")

        # 判断是否结束
        if check_winning(attacker_usvs):
            hint = HostMsg(content="Attackers win!")
            break


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    main()

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
