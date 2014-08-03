import xml.etree.ElementTree as ET
import pygame
from itertools import *
import struct

def get_tiled(path):
    xml_context = parseTMX(path)
    tiled = Tiled(xml_context)
    return tiled


class Tiled:
    def __init__(self, xml_context):
        self.orientation = xml_context.attrib["orientation"]

        self.grid_size = (int(xml_context.attrib['width']), int(xml_context.attrib['height']))
        self.tile_size = (int(xml_context.attrib['tileheight']), int(xml_context.attrib['tilewidth']))

        self.tileSetGroup = TileSetGroup(self.tile_size)
        for tileset_context in xml_context.iter("tileset"):
            self.tileSetGroup.append(TileSet(tileset_context))

        self.layers = [Layer(layer_context, self.tileSetGroup) for layer_context in xml_context.iter("layer")]

    def __iter__(self):
        return iter(self.layers)


class Layer:
    def __init__(self, layer_context, tileSetGroup):
        # image manager or tilesets group provides image by index - id
        self.image_manager = tileSetGroup

        self.tile_size = self.image_manager.tile_size

        #general properties
        self.name = layer_context.attrib['name']
        self.width = int(layer_context.attrib['width'])
        self.height  = int(layer_context.attrib['height'])

        #custom properties
        for properties in layer_context.iter("properties"):
            for property in properties:
                property_dict = property.attrib
                if "name" in property_dict and "value" in property_dict:
                    setattr(self, property_dict["name"], property_dict["value"])

        #data
        data = list(self.__parseDate(layer_context.find("data")))
        self.cells = self.__generate_cells(data)


    def __parseDate(self, data):
        throw_if_none('layer %s does not contain <data>' % self.name)

        data = data.text.strip()
        data = data.decode('base64').decode('zlib')
        data = struct.unpack('<%di' % (len(data)/4,), data)

        return zip(*[data[i * self.width: (i + 1) * self.width] for i in range(self.height)])


    def __generate_cells(self, data):
        layer_group = pygame.sprite.Group()
        for i in range(self.width):
            for j in range(self.height):
                print i, j
                image_index = data[i][j]
                if image_index != 0:
                    cell = Cell()
                    cell.image = self.image_manager.get_image(image_index)
                    tile_size = cell.image.get_size()
                    cell.rect = pygame.Rect( i * tile_size[0], j * tile_size[1], *tile_size)
                    layer_group.add(cell)
        return layer_group

class TileSetGroup:
    """
    Class-container for TitleSet with unified index getter.
    """
    #TODO fix arg and add assert or raise error exception if tile_size doesn't match
    def __init__(self, tile_size,*arg):
        self.tile_size = tile_size
        self.tilesets = list(arg)

    def append(self, tileset):
        self.tilesets.append(tileset)
        print self.tilesets


    def get_image(self, index):
        for tileset in self.tilesets:
            if tileset.check_image_index(index):
                return tileset.get_image(index)
        raise ValueError("Tileset {} hadn't been found".format(index))


class TileSet:
    def __init__(self, tile_set_context):
        self.tile_size = (int(tile_set_context.attrib['tilewidth']), int(tile_set_context.attrib['tileheight']))

        image_context = tile_set_context.find("image")
        self.image_size = (int(image_context.attrib["width"]), int(image_context.attrib["height"]))
        self.image = pygame.image.load(open(image_context.attrib["source"]))

        # for saving already processed sub image in get_image method
        self.subimages = {}

        self.firstgid = int(tile_set_context.attrib['firstgid'])
        self.lastgid = self.firstgid + (self.image_size[0] * self.image_size[1]) / (self.tile_size[0] * self.tile_size[1])


    def get_image(self, index):
        assert self.check_image_index(index)
        if index not in self.subimages:
            self.subimages[index] = self.image.subsurface(self.__get_sub_rect(index - self.firstgid))
        return self.subimages[index]

    def check_image_index(self, index):
        return self.firstgid <= index < self.lastgid

    def __get_sub_rect(self, index):
        start_x = index * self.tile_size[0] % self.image_size[0]
        start_y = index * self.tile_size[1] / self.image_size[1]
        return pygame.Rect(start_x, start_y, *self.tile_size)



class Cell(pygame.sprite.Sprite):
    def __int__(self):
        pygame.sprite.Sprite.__init__(self)

    def update(self, dt):
        pass


def throw_if_none(what, message=None):
    if what is None:
        raise ValueError(message)


def parseTMX(path):
    tree = ET.parse(path)
    root = tree.getroot()
    return root

if __name__== "__main__":
    parsed_tiled("../tiled/level1.tmx")

