# Filtering functions
operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                return name, operator_type[0].strip(), value

    return [None] * 3


# Styling functions
def style_title():
    title_style = {
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    }
    return title_style

def style_font():
    font_style = {
        'family': "Raleway"
    }
    return font_style

def network_layout_options():
    options = [
        {'label' : 'Circular', 'value' : 'circular'},
        {'label' : 'Kamada-Kawai', 'value' : 'kamada-kawai'},
        {'label' : 'Random', 'value' : 'random'},
        {'label' : 'Shell', 'value' : 'shell'},
        {'label' : 'Spring', 'value' : 'spring'},
        {'label' : 'Spectral', 'value' : 'spectral'}
    ]
    return options

def generate_options(option_arr):
    return [{'label' : str(option).title(), 'value' : option} for option in option_arr]

def generate_range_values(value_arr):
    return {i : str(value_arr[i]) for i in range(len(value_arr))}