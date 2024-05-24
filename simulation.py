import matplotlib.pyplot as plt
import imageio
import numpy as np

# 读取文件内容
file_path = 'txt_gif/file-20240524120425'
with open(file_path+".txt", 'r') as file:
    lines = file.readlines()

# 解析数据
rounds = []
players = set()
for line in lines:
    parts = line.split(':', 1)
    round_num = int(parts[0].split()[1])
    round_data = {}
    parts = parts[1].split(';')
    for part in parts:
        if not part.startswith('Player'):
            continue
        player, coords = part.split(':')
        coords = coords.strip().strip('()').split(', ')
        round_data[player] = (float(coords[0]), float(coords[1]))
        players.add(player)
    rounds.append(round_data)

trajectories = {player: [] for player in players}
# 创建绘图并生成GIF
filenames = []
for i, round_data in enumerate(rounds):
    plt.figure(figsize=(8, 8))
    ax = plt.gca()

    # 画圆
    circle = plt.Circle((0, 0), 5, color='blue', fill=False)
    ax.add_patch(circle)

    # 更新轨迹数据
    for player, (x, y) in round_data.items():
        trajectories[player].append((x, y))

    # 画轨迹和每个Player的位置
    for player, trajectory in trajectories.items():
        xs, ys = zip(*trajectory)
        color = 'red' if int(player[-1]) <= 3 else 'blue'
        plt.plot(xs, ys, '-', color=color)
        plt.plot(xs[-1], ys[-1], 'o', label=player, color=color)

    plt.xlim(-15, 15)
    plt.ylim(-15, 15)
    plt.xlabel('X coordinate')
    plt.ylabel('Y coordinate')
    plt.legend()
    plt.title(f'Round {i + 1}')

    filename = f'simulation/round_{i + 1}.png'
    plt.savefig(filename)
    filenames.append(filename)
    plt.close()

# 创建GIF
with imageio.get_writer(f'{file_path}.gif', mode='I', duration=0.5) as writer:
    for filename in filenames:
        image = imageio.v2.imread(filename)
        writer.append_data(image)

print("GIF生成完毕！")