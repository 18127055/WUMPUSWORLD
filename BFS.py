
import agent as a

def sln(trace,moveable_pos):
    i, path = moveable_pos, []
    while i != -1:
        path.append(i)
        i = trace[i[0]][i[1]]
    path.reverse()
    path.pop(0)
    return path

def A_star(maze,moveable_pos, cur):
    fo = moveable_pos
    h0 = a.manhattan(cur, fo)
    frontier, explored, trace = [[cur, h0]], [], [
        [-1 for _ in range(10)] for _ in range(10)]
    dist = 0
    while len(frontier) != 0:
        frontier = sorted(frontier, key=lambda tup: (tup[1]))
        t = frontier.pop(0)
        explored.append(t[0])
        tem_front = [i[0] for i in frontier]
        if t[0] == fo:
            return sln(trace,moveable_pos)
        dist += 1
        if t[0][0]-1 >= 0:  # up
            if maze[t[0][0]-1][t[0][1]][5] == 1:
                if (t[0][0]-1, t[0][1]) not in tem_front and (t[0][0]-1, t[0][1]) not in explored:
                    trace[t[0][0]-1][t[0][1]] = t[0]
                    h1 = a.manhattan((t[0][0]-1, t[0][1]), fo)
                    f1 = dist + h1
                    frontier.append([(t[0][0]-1, t[0][1]), f1])
                elif (t[0][0]-1, t[0][1]) in tem_front and dist + a.manhattan((t[0][0]-1, t[0][1]), fo) < frontier[tem_front.index((t[0][0]-1, t[0][1]))][1]:
                    trace[t[0][0]-1][t[0][1]] = t[0]
                    del frontier[tem_front.index((t[0][0]-1, t[0][1]))]
                    f1 = dist + a.manhattan((t[0][0]-1, t[0][1]), fo)
                    frontier.insert((t[0][0]-1, t[0][1]), f1)
        if t[0][0]+1 < 10:  # down
            if maze[t[0][0]+1][t[0][1]][5] == 1:
                if (t[0][0]+1, t[0][1]) not in tem_front and (t[0][0]+1, t[0][1]) not in explored:
                    trace[t[0][0]+1][t[0][1]] = t[0]
                    h1 = a.manhattan((t[0][0]+1, t[0][1]), fo)
                    f1 = dist + h1
                    frontier.append([(t[0][0]+1, t[0][1]), f1])
                elif (t[0][0]+1, t[0][1]) in tem_front and dist + a.manhattan((t[0][0]+1, t[0][1]), fo) < frontier[tem_front.index((t[0][0]+1, t[0][1]))][1]:
                    trace[t[0][0]+1][t[0][1]] = t[0]
                    del frontier[tem_front.index((t[0][0]+1, t[0][1]))]
                    f1 = dist + a.manhattan((t[0][0]+1, t[0][1]), fo)
                    frontier.insert((t[0][0]+1, t[0][1]), f1)
        if t[0][1]+1 < 10:  # right
            if maze[t[0][0]][t[0][1]+1][5] == 1:
                if (t[0][0], t[0][1]+1) not in tem_front and (t[0][0], t[0][1]+1) not in explored:
                    trace[t[0][0]][t[0][1]+1] = t[0]
                    h1 = a.manhattan((t[0][0], t[0][1]+1), fo)
                    f1 = dist + h1
                    frontier.append([(t[0][0], t[0][1]+1), f1])
                elif (t[0][0], t[0][1]+1) in tem_front and dist + a.manhattan((t[0][0], t[0][1]+1), fo) < frontier[tem_front.index((t[0][0], t[0][1]+1))][1]:
                    trace[t[0][0]][t[0][1]+1] = t[0]
                    del frontier[tem_front.index((t[0][0], t[0][1]+1))]
                    f1 = dist + a.manhattan((t[0][0], t[0][1]+1), fo)
                    frontier.insert((t[0][0], t[0][1]+1), f1)
        if t[0][1]-1 >= 0:  # left
            if maze[t[0][0]][t[0][1]-1][5] == 1:
                if (t[0][0], t[0][1]-1) not in tem_front and (t[0][0], t[0][1]-1) not in explored:
                    trace[t[0][0]][t[0][1]-1] = t[0]
                    h1 = a.manhattan((t[0][0], t[0][1]-1), fo)
                    f1 = dist + h1
                    frontier.append([(t[0][0], t[0][1]-1), f1])
                elif (t[0][0], t[0][1]-1) in tem_front and dist + a.manhattan((t[0][0], t[0][1]-1), fo) < frontier[tem_front.index((t[0][0], t[0][1]-1))][1]:
                    trace[t[0][0]][t[0][1]-1] = t[0]
                    del frontier[tem_front.index((t[0][0], t[0][1]-1))]
                    f1 = dist + a.manhattan((t[0][0], t[0][1]-1), fo)
                    frontier.insert((t[0][0], t[0][1]-1), f1)
    return
