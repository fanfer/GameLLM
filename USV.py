import math

from agentscope.agents import AgentBase


class USV:
    usvs = []
    defend_radius = 1
    circle_radius = 10
    circle_center = (0, 0)

    def __init__(self, name: str, role: str, x: float, y: float, agent: AgentBase):
        self.name = name
        self.role = role
        self.x = x
        self.y = y
        self.agent = agent
        self._distance_max = 1

    # 向angle方向移动distance距离
    def move(self, distance, angle) -> bool:
        _x = self.x + distance * math.cos(angle)
        _y = self.y + distance * math.sin(angle)
        if self.role == "attacker":
            for usv in self.usvs[3:]:
                if usv == self:
                    continue
                distance = math.sqrt((_x - usv.x) ** 2 + (_y - usv.y) ** 2)
                if distance < self.defend_radius:
                    return False
        self.x = _x
        self.y = _y
        return True
