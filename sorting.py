def sort_children(elements, xy, mode="v", align="center", gap=5):
    x,y = xy
    if mode == "v":
        for i,e in enumerate(elements):
            if i > 0:
                e.set_topleft(None, elements[i-1].rect.bottom + gap)
            else: #first element to be sorted
                e.set_topleft(None, y)
            if align == "center":
                e.set_center(x, e.rect.centery)
            elif align == "left":
                e.set_topleft(x, None)
            elif align == "right":
                e.set_bottomright(x, e.rect.bottom)
            else:
                raise ValueError("'align' argument for vertical mode must be either 'left', 'center' or 'right'")
    elif mode == "h":
        for i,e in enumerate(elements):
            if i > 0:
                e.set_topleft(elements[i-1].rect.right + gap, None)
            else:
                e.set_topleft(x, None)
            if align == "center":
                e.set_center(e.rect.centerx, y)
            elif align == "top":
                e.set_topleft(None, y)
            elif align == "bottom":
                e.set_bottomright(e.rect.right, y)
            else:
                raise ValueError("'align' argument for horizontal mode must be either 'top', 'center' or 'bottom'")
    else:
        raise ValueError("'mode' argument must be either 'v' or "+\
                         "'h'.")

def sort_children_grid(els, xy, nx, ny, cellsize, horizontal_first=True, gap_x=5, gap_y=5):
    if nx == "auto" and ny == "auto":
        nx = ny = int(len(els)**0.5) + 1
    elif nx == "auto":
        nx = len(els) // ny + 1
    elif ny == "auto":
        ny = len(els) // nx + 1
    x = 0
    y = 0
    # max_w = max([e.rect.width for e in els])
    # max_h = max([e.rect.height for e in els])
    max_w, max_h = cellsize
    for e in els:
        if horizontal_first and x > nx:
            x = 0
            y += 1
        elif y >= ny:
            y = 0
            x += 1
        cx = x*(max_w + gap_x) + xy[0]
        cy = y*(max_h + gap_y) + xy[1]
##        e.rect.center = (cx, cy)
        e.set_center(cx,cy)
        if horizontal_first:
            x += 1
        else:
            y += 1


def get_side_center(r, side):
    if side == "top":
        x0,y0 = r.centerx, r.top
    elif side == "bottom":
        x0,y0 = r.centerx, r.bottom
    elif side == "left":
        x0,y0 = r.x, r.centery
    elif side == "right":
        x0,y0 = r.right, r.centery
    return x0,y0