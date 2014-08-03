import xml.etree.ElementTree as ET
import pygame
import itertools


class Tileset:
    def __init__(self, tileset):
        print tileset.attrib
        image_element = tileset.find("image")
        print image_element.attrib
        width = int(image_element.attrib['width'])
        height = int(image_element.attrib['height'])
        tileheight = int(tileset.attrib['tileheight'])
        tilewidth = int(tileset.attrib['tilewidth'])
        firstgid = int(tileset.attrib['firstgid'])

        image = pygame.image.load(image_element.attrib["source"])
        images = {}

        start_coords = list(itertools.product(range(0, width, tilewidth), range(0, height, tileheight)))

        for index, (x, y) in enumerate(start_coords, start=firstgid):
                images[index] = image.subsurface(pygame.Rect(x, y, tilewidth, tileheight))


class Layer:
    def __init__(self, layer):
        name = layer.attrib("name")


def parseTMX(path):
    tree = ET.parse(path)
    root = tree.getroot()

    width = int(root.attrib['width'])
    height = int(root.attrib['height'])
    tileheight = int(root.attrib['tileheight'])
    tilewidth = int(root.attrib['tilewidth'])

    for tileset in root.findall("tileset"):
        tileset = Tileset(tileset)

#    for tileset in root.findall("layer"):
 #       print tileset.attrib

    return root

parseTMX("D:/maynard/PlatformerFire/tiled/level1.tmx")
