import xml.etree.ElementTree as ET
import pygame
import struct
import os
import auxiliary


def get_tiled(path):
    xml_context = parse_tmx(path)
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
    def __init__(self, layer_context, tile_set_group):
        # image manager or tilesets group provides image by index - id
        self.image_manager = tile_set_group

        self.tile_size = self.image_manager.tile_size

        #general properties
        self.name = layer_context.attrib['name']
        self.width = int(layer_context.attrib['width'])
        self.height = int(layer_context.attrib['height'])

        #custom properties
        for properties in layer_context.iter("properties"):
            for _property in properties:
                property_dict = _property.attrib
                if "name" in property_dict and "value" in property_dict:
                    setattr(self, property_dict["name"], property_dict["value"])

        #data
        data = list(self.__parse_data(layer_context.find("data")))
        self.cells = self.__generate_cells(data)

    def __parse_data(self, data):
        throw_if_none('layer %s does not contain <data>' % self.name)

        data = data.text.strip()
        data = data.decode('base64').decode('zlib')
        data = struct.unpack('<%di' % (len(data)/4,), data)

        data = zip(*[data[i * self.width: (i + 1) * self.width] for i in range(self.height)])
        print zip(*data)[-4]
        return data

    def __generate_cells(self, data):
        layer_group = pygame.sprite.Group()
        for i in range(self.width):
            for j in range(self.height):
                image_index = data[i][j]
                if image_index != 0:
                    cell = Cell()
                    setattr(cell, "image", self.image_manager.get_image(image_index))
                    tile_size = cell.image.get_size()
                    setattr(cell, "rect", pygame.Rect(i * tile_size[0], j * tile_size[1], *tile_size))
                    layer_group.add(cell)
        return layer_group


class TileSetGroup:
    """
    Class-container for TitleSet with unified index getter.
    """
    #TODO fix arg and add assert or raise error exception if tile_size doesn't match
    def __init__(self, tile_size, *arg):
        self.tile_size = tile_size
        self.tilesets = list(arg)

    def append(self, tileset):
        self.tilesets.append(tileset)

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
        image_path = os.path.abspath(image_context.attrib["source"])
        self.image = pygame.image.load(image_path).convert_alpha()

        # for saving already processed sub image in get_image method
        self.sub_images = {}

        self.first_image_id = int(tile_set_context.attrib['firstgid'])

    def get_image(self, index):
        assert self.check_image_index(index)
        if index not in self.sub_images:
            self.sub_images[index] = self.image.subsurface(self.__get_sub_rect(index - self.first_image_id))
        return self.sub_images[index]

    def check_image_index(self, index):
        return self.first_image_id <= index < self.last_image_id

    def __get_sub_rect(self, index):
        local_index = self._index_to_local(index)
        return pygame.Rect(auxiliary.multiply(local_index, self.tile_size), self.tile_size)

    @property
    def last_image_id(self):
        return self.first_image_id + (self.image_size[0] * self.image_size[1]) / (self.tile_size[0] * self.tile_size[1])

    def _index_to_local(self, index):
        image_capacity = auxiliary.division(self.image_size, self.tile_size)
        return index % image_capacity[0], index // image_capacity[1]


class Cell(pygame.sprite.Sprite):
    def __int__(self):
        pygame.sprite.Sprite.__init__(self)

    def update(self, dt):
        pass


def throw_if_none(what, message=None):
    if what is None:
        raise ValueError(message)


def parse_tmx(path):
    tree = ET.parse(path)
    root = tree.getroot()
    return root
