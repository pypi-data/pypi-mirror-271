import pickle
from magictk import photoload
from magictk import color_tmpl


def set_color_style(color_set={}, **kwargs):
    if color_set == {}:
        color_tmpl.default_color.update(kwargs)
    else:
        color_tmpl.default_color.update(color_set)


def load_icon_pack(path):
    with open(path, "rb") as file:
        photoload.image_all.update(pickle.load(file))
