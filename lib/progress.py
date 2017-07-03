def progress(
        display,
        x, y, width,
        v_min=0, v_max=100,
        initial_value=0,
        suffix='%', prefix='',
        color=1
    ):

    from d2 import scale_linear
    y_scale = scale_linear(v_min, v_max, x+1, x+width-2)

    def update(value, frame=False):
        if frame:
            display.rect(x, y, width, 10, color)
        display.fill_rect(x+1, y+1, y_scale(v_max), 8, 0)
        display.text(prefix+str(value)+suffix, x+1, y+1, color)
        display.invert_rect(x+1, y+1, y_scale(value), 8)

    update(initial_value, True)

    return update