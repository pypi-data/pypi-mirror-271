#from awpy.data import NAV, MAP_DATA
import plotly.graph_objects as go
import plotly.express as px
from PIL import ImageDraw
import os
from cs_bahtml.radars import MAP_DATA

def fill_area(fig,mapname=None,areaId=None):
    if areaId:
        fig = go.Figure(fig)
        area = NAV[mapname][areaId]
        fig.add_shape(type="rect",
            x0=area["southEastX"], 
            y0=area["southEastY"], 
            x1=area["northWestX"], 
            y1=area["northWestY"],
            fillcolor="LightSkyBlue"
        )
    return fig



def position_transform(mapname, position, axis):
    start_x = MAP_DATA[mapname]["pos_x"]
    start_y = MAP_DATA[mapname]["pos_y"]
    scale = MAP_DATA[mapname]["scale"]
    if axis == "x":
        return (position - start_x) / scale
    elif axis == "y":
        return (start_y- position) / scale
    else:
        raise ValueError("Axis must be x or y")




def generate_contour(fig,dff,mapname,type="contour"):

    x = dff.opponentArea_rotated_x.apply(lambda x: position_transform(mapname, x, "x"))
    y = dff.opponentArea_rotated_y.apply(lambda x: position_transform(mapname, x, "y"))

    fig.data = [fig.data[0]]

    if type=="contour" or type=="both":
        fig.add_trace(go.Histogram2dContour(
        x = x,
        y = y,
        opacity = .25,
        ncontours=10,
        histnorm= "probability",
        xbins= dict(start=0, end = 1024, size=32),
        ybins= dict(start=0, end = 1024, size=32),
        colorscale=[[1, 'rgba(214, 39, 40, 1)'],   
                [0, 'rgba(128, 128, 128, 1)']],
        xaxis = 'x',
        line = dict(smoothing=0.5),
        yaxis = 'y',
        showscale=False,
        hoverinfo='skip'
        ))
    if type=="scatter" or type=="both":
        fig.add_trace(go.Scatter(
        x = x,
        y = y,
        opacity = .50,
        #histnorm="probability density",
        #ncontours=30,
        #colorscale=[[1, 'rgba(214, 39, 40, 0.85)'],   
        #        [0.1, 'rgba(128, 128, 128, 0)']],
        xaxis = 'x',
        yaxis = 'y',
        mode='markers',
        #showscale=False,
        hoverinfo='skip'
        ))



    return fig
util_rad = {
    'molotov':100,
    'smoke':144
}
def add_smoke_wall(fig,smokes, mapname, type):
    
    rad = position_transform(mapname, util_rad[type], "x") - position_transform(mapname, 0, "x")
    for x,y,z in smokes:
        x = position_transform(mapname, x, 'x')
        y = position_transform(mapname, y, 'y')
        fig = add_smoke(fig,x, y, rad, type)
    return fig

def add_players(fig, players, mapname,type):
    player_rad = position_transform(mapname, 60, "x") - position_transform(mapname, 0, "x")
    for x,y,z in players:
        x = position_transform(mapname, x, 'x')
        y = position_transform(mapname, y, 'y')
        fig = add_player(fig,x, y, player_rad, type = type)
    return fig

util_color = {
    'molotov':'rgb(255,119,0)',
    'smoke':'rgb(128,128,128)'
}

def add_smoke(fig, x, y, smoke_rad, type):
    draw = ImageDraw.Draw(fig)
    draw.ellipse(
        xy= [(x-smoke_rad,y-smoke_rad), (x+smoke_rad,y+smoke_rad)],
                outline='rgb(12,15,18)',
                fill= util_color[type]
    )

    return fig
player_color = {
    'CT':'rgb(93,121,174)',
    'TERRORIST':'rgb(204,186,124)',
    'thrower':'rgba(0,128,0,50)',
}
def add_player(fig,x,y, player_rad, type):
    draw = ImageDraw.Draw(fig)
    linecol = 'rgb(12,15,18)'
    
    if type.startswith("dead"):
        side = type.split("_")[-1]
        width = int(player_rad/10)
        draw.line(
            xy= [(x-player_rad,y-player_rad), (x+player_rad,y+player_rad)],
            width = width,
            fill= player_color[side]
        )
        draw.line(
            xy= [(x-player_rad,y+player_rad), (x+player_rad,y-player_rad)],
            width = width,
            fill= player_color[side]
        )
    else:
        draw.ellipse(
            xy= [(x-player_rad,y-player_rad), (x+player_rad,y+player_rad)],
                    outline=linecol,
                    fill= player_color[type]
        )
    return fig