dir_dict = {'l':(-1, 0), 'r':(1, 0), 'u':(0, -1), 'd':(0, 1)}
dict_dir = {(-1, 0):'l', (1, 0):'r', (0, -1):'u', (0, 1):'d'}

# [mx, my, width, height]
#['dir', [x, y]]
def path_to_rect(a, b, cell_size):
    mx = min(a[1][0], b[1][0])
    my = min(a[1][1], b[1][1])

    if a[0] == 'r' or a[0] == 'l':
        return (mx, my, abs((a[1][0]) - (b[1][0])), cell_size)

    return (mx, my, cell_size, abs((a[1][1]) - (b[1][1])))
