from types import SimpleNamespace
from decimal import *
from src.API.DiGraph import DiGraph
from src.API.GraphAlgo import GraphAlgo
from src.Game.client import Client
import json
import time as t
from pygame import gfxdraw
import pygame
from pygame import *
from src.API import *

# init pygame
WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()

client = Client()
client.start_connection(HOST, PORT)

pokemons = client.get_pokemons()
pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))

print(pokemons)

graph_json = client.get_graph()

FONT = pygame.font.SysFont('Arial', 20, bold=True)
# load the json string into SimpleNamespace Object

graph = json.loads(graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))

for n in graph.Nodes:
    x, y, _ = n.pos.split(',')
    n.pos = SimpleNamespace(x=float(x), y=float(y))

# get data proportions
min_x = min(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
min_y = min(list(graph.Nodes), key=lambda n: n.pos.y).pos.y
max_x = max(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
max_y = max(list(graph.Nodes), key=lambda n: n.pos.y).pos.y


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


# decorate scale with the correct values
def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


radius = 15

client.add_agent("{\"id\":0}")
client.add_agent("{\"id\":1}")
client.add_agent("{\"id\":2}")
client.add_agent("{\"id\":3}")

# This commnad starts the server - the game is running now
client.start()
my_graph = DiGraph.DiGraph()
my_a_graph = GraphAlgo.GraphAlgo()
my_a_graph.load_from_json(client.get_graph())

# Save the original values
dict = {}


# Draw the button with the data
def draw_button(button, screen):
    pygame.draw.rect(screen, button['color'], button['rect'])
    screen.blit(button['text'], button['text rect'])


# Butten to stop quit the game
def init_button(val_x, val_y, val_w, val_h, text, call):
    text_font = FONT.render(text, True, (255, 255, 255))
    button_rect = pygame.Rect(val_x, val_y, val_w, val_h)
    text_rect = text_font.get_rect(center=button_rect.center)
    button = {'text': text_font, 'rect': button_rect, 'call': call, 'text rect': text_rect,
              'color': (142, 141, 203)}
    return button


def stop():
    display.update()
    client.stop()
    pygame.quit()
    exit(0)


def get_which_edge(x_pok: float, y_pok: float, type: int) -> (float, float):
    for edge in graph.Edges:
        x_src = my_a_graph.nodes_data_pos(edge.src)[0]
        y_src = my_a_graph.nodes_data_pos(edge.src)[1]
        x_dest = my_a_graph.nodes_data_pos(edge.dest)[0]
        y_dest = my_a_graph.nodes_data_pos(edge.dest)[1]
        slope = (Decimal(y_src) - Decimal(y_dest)) / (Decimal(x_src) - Decimal(x_dest))
        b = Decimal(y_src) - (Decimal(x_src) * Decimal(slope))
        b_pock = Decimal(y_pok) - (Decimal(x_pok) * Decimal(slope))
        if abs(b - b_pock) < 0.0000001:
            if type > 0:
                return edge.src, edge.dest
            return edge.dest, edge.src


curr_color = (237, 255, 253)
quit_button = init_button(Rect(430, 600, 100, 100).x + 450, Rect(430, 600, 100, 100).y, 180, 50, 'OUT OF THE GAME!',
                          stop)

while client.is_running() == 'true':
    pokemons = json.loads(client.get_pokemons(), object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pokemons = [p.Pokemon for p in pokemons]
    index = 0
    for p in pokemons:
        x, y, _ = p.pos.split(',')
        dict[index] = (x, y, int(p.type))
        index = index + 1
        p.pos = SimpleNamespace(x=my_scale(float(x), x=True), y=my_scale(float(y), y=True))

    agents = json.loads(client.get_agents(), object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]

    for a in agents:
        x, y, _ = a.pos.split(',')
        a.pos = SimpleNamespace(x=my_scale(float(x), x=True), y=my_scale(float(y), y=True))
    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if quit_button['rect'].collidepoint(event.pos):
                    quit_button['call']()

    # refresh surface
    screen.fill(Color(139, 112, 121))

    # Get score
    info = json.loads(client.get_info())
    score = info.get("GameServer")["grade"]
    score_info = FONT.render(f"Score: {score}", True, curr_color)
    rect = score_info.get_rect(center=(100, 10))
    screen.blit(score_info, rect)

    # Get moves
    moves = info.get("GameServer")["moves"]
    moves_info = FONT.render(f"Moves: {moves}", True, curr_color)
    rect = moves_info.get_rect(center=(100, 50))
    screen.blit(moves_info, rect)

    # Get time to finish
    time_to_finish = Decimal(client.time_to_end()) / 1000
    time_info = FONT.render(f"Time To Finish: {int(time_to_finish)}", True, curr_color)
    rect = time_info.get_rect(center=(100, 100))
    screen.blit(time_info, rect)

    # draw nodes
    for n in graph.Nodes:
        x = my_scale(n.pos.x, x=True)
        y = my_scale(n.pos.y, y=True)

        # its just to get a nice antialiased circle
        gfxdraw.filled_circle(screen, int(x), int(y), radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y), radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # draw edges
    for e in graph.Edges:
        # find the edge nodes
        src = next(n for n in graph.Nodes if n.id == e.src)
        dest = next(n for n in graph.Nodes if n.id == e.dest)

        # scaled positions
        src_x = my_scale(src.pos.x, x=True)
        src_y = my_scale(src.pos.y, y=True)
        dest_x = my_scale(dest.pos.x, x=True)
        dest_y = my_scale(dest.pos.y, y=True)

        # draw the line
        pygame.draw.line(screen, Color(61, 72, 126), (src_x, src_y), (dest_x, dest_y))

    # draw agents
    for agent in agents:
        pygame.draw.circle(screen, Color(240, 240, 240), (int(agent.pos.x), int(agent.pos.y)), 10)

    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in pokemons:
        pygame.draw.circle(screen, Color(0, 255, 255), (int(p.pos.x), int(p.pos.y)), 10)

    draw_button(quit_button, screen)

    # update screen changes
    display.update()

    # refresh rate
    clock.tick(60)

    # choose next edge
    for agent in agents:
        if agent.dest == -1:
            mindist = 1000000
            next_node = agent.src
            i = 0
            for poke in pokemons:
                print(dict)
                edge = get_which_edge(dict[i][0], dict[i][1], dict[i][2])
                tmpDist, tmpLst = my_a_graph.shortest_path(agent.src, int(edge[0]))
                if tmpDist == 0:
                    next_node = int(edge[1])
                    break
                if tmpDist < mindist:
                    mindist = tmpDist
                    next_node = tmpLst[1]
                i = i + 1
            client.choose_next_edge(
                '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())

    client.move()
    t.sleep(0.1)
    # game over:
