from file_finder.utils import find_by_name, find_by_ext, find_by_mod

SEARCH_MAPPING = {
        "name": find_by_name,
        "ext": find_by_ext,
        "mod": find_by_mod
    }

TABLE_HEADRES = ["Name", "Ext", "Mod", "Location"]