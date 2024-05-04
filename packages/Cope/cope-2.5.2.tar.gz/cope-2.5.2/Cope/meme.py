from .imports import try_import
from io import BytesIO
from importlib import resources as impresources
from . import assets


def look_at_this_graph(graph, fudge=(0, 28)):
    """ LOOK AT THIS _____GRAPH!!! """
    from PIL import Image
    from PIL import ImageOps
    matplotlib = try_import('matplotlib')
    plotly = try_import('plotly')

    template = Image.open(impresources.files(assets) / 'look at this photograph template.png')
    mask = Image.open(impresources.files(assets) / 'look at this photograph mask.png').convert('L')

    try:
        is_matplotlib = isinstance(graph, matplotlib.figure.Figure)
    except:
        is_matplotlib = False

    if matplotlib and is_matplotlib:
        graph.canvas.draw()
        raw_graph = Image.frombytes('RGB', graph.canvas.get_width_height(), graph.canvas.tostring_rgb())
    elif type(graph) is str:
        try:
            raw_graph = Image.open(graph)
        except:
            raise ValueError(f"Can't open file {graph}")
    elif type(graph) is bytes:
        raw_graph = Image.open(BytesIO(graph))
    elif plotly and type(graph) is plotly.graph_objs._figure.Figure:
        raw_graph = Image.open(BytesIO(plotly.io.to_image(graph, 'png', width=template.width, height=template.height)))
    else:
        raise ValueError(f"Graph type `{type(graph)}` not supported. Supported types are matplotlib, plotly, bytes, and filepaths")

    # Resize, pad, rotate, and shift the graph
    new_size = template.size
    padding_color = (255, 255, 255)
    graph_size = (343, 213)

    raw_graph = raw_graph.resize(graph_size)

    # Resize and pad the image
    resized_image = ImageOps.expand(raw_graph, (
            (new_size[0] - raw_graph.width)  // 2,
            (new_size[1] - raw_graph.height) // 2
        ),
        fill=padding_color
    )

    # In degrees
    rotation_angle = 13.3

    # Rotate the original image
    rotated_image = raw_graph.rotate(rotation_angle, expand=True, fillcolor=padding_color)

    # Calculate the shift
    shift = (476 + fudge[0], 247 - (round(graph_size[1]/2)) + fudge[1])

    # Create a new image with the padded size
    adj_graph = Image.new("RGB", new_size, padding_color)

    # Paste the rotated image onto the final image with the desired shift
    adj_graph.paste(rotated_image, shift)
    adj_graph

    return Image.composite(adj_graph, template, mask)
