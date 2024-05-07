from collections import UserList
from weakref import WeakSet
from typing import Type
from colorlog import getLogger

from . import config
from .data_model import data_models
from .utils import *
from .default_types import ComponentList, component_list_map, ComponentDictionary, component_dict_map

from .simultan_object import SimultanObject
from .geometry.utils import create_python_geometry

from SIMULTAN.Data.Geometry import (Layer, Vertex, Edge, PEdge, Face, Volume, EdgeLoop)
from .geometry.geometry_base import (SimultanLayer, SimultanVertex, SimultanEdge, SimultanEdgeLoop, SimultanFace,
                                     SimultanVolume)

logger = getLogger('PySimultan')

default_registered_classes = {'ComponentList': ComponentList,
                              'ComponentDict': ComponentDictionary}
default_mapped_classes = {}
default_taxonomy_maps = {'ComponentList': component_list_map,
                         'ComponentDict': component_dict_map}


class PythonMapper(object):

    def __new__(cls, *args, **kwargs):
        instance = super(PythonMapper, cls).__new__(cls)
        config.default_mapper = instance
        return instance

    def __init__(self, *args, **kwargs):
        self.registered_classes = default_registered_classes   # dict with all registered classes: {taxonomy: class}
        self.mapped_classes = default_mapped_classes           # dict with all mapped classes: {taxonomy: class}
        self.taxonomy_maps = default_taxonomy_maps             # dict with all taxonomie maps: {taxonomy: taxonomie_map}

        self.registered_geometry_classes = {Layer: SimultanLayer,
                                            Vertex: SimultanVertex,
                                            Edge: SimultanEdge,
                                            Face: SimultanFace,
                                            Volume: SimultanVolume,
                                            EdgeLoop: SimultanEdgeLoop}

        self.re_register = False

    def register(self, taxonomy, cls, taxonomy_map=None):
        if not self.re_register and taxonomy in self.registered_classes.keys():
            return

        self.registered_classes[taxonomy] = cls
        self.taxonomy_maps[taxonomy] = taxonomy_map

    def create_mapped_class(self, taxonomy, cls):

        if any([issubclass(cls, x) for x in (SimultanObject, UserList)]):
            bases = (cls,)
        else:
            bases = (SimultanObject,) + (cls,)

        def new_init(self, *args, **kwargs):
            for base in self.__class__.__bases__:
                base.__init__(self, *args, **kwargs)

        new_class_dict = {'__init__': new_init,
                          '__name__': cls.__name__,
                          '_taxonomy': taxonomy,
                          '_taxonomy_map': self.taxonomy_maps.get(taxonomy, None),
                          '_base': bases,
                          '_object_mapper': self}

        new_class_dict.update(self.get_properties(taxonomy))
        new_class = type(cls.__name__, bases, new_class_dict)

        self.mapped_classes[taxonomy] = new_class

        return new_class

    def get_mapped_class(self, taxonomy) -> Type[SimultanObject]:
        if self.mapped_classes.get(taxonomy, None) is None:
            self.create_mapped_class(taxonomy, self.registered_classes[taxonomy])

        return self.mapped_classes.get(taxonomy, None)

    def get_typed_data(self, data_model=None, component_list=None, create_all=False):

        typed_data = []

        if component_list is None:
            component_list = list(data_model.data.Items)

        if data_model is None:
            data_model = list(data_models)[0]

        for component in component_list:
            typed_object = self.create_python_object(component, data_model=data_model)
            typed_data.append(typed_object)
            if create_all:

                def get_content(typed_object):
                    if isinstance(typed_object, SimultanObject):
                        for content in typed_object.__class__._taxonomy_map.content:
                            val = getattr(typed_object, content.property_name)
                            if isinstance(val, (SimultanObject, ComponentList, ComponentDictionary)):
                                typed_data.append(val)
                                get_content(val)
                    elif isinstance(typed_object, ComponentList):
                        for item in typed_object:
                            if isinstance(item, (SimultanObject, ComponentList, ComponentDictionary)):
                                typed_data.append(item)
                                get_content(item)
                    elif isinstance(typed_object, ComponentDictionary):
                        for item in typed_object.values():
                            if isinstance(item, (SimultanObject, ComponentList, ComponentDictionary)):
                                typed_data.append(item)
                                get_content(item)

                get_content(typed_object)

        return typed_data

    # @lru_cache(maxsize=None)
    def create_python_object(self, component, cls=None, data_model=None, *args, **kwargs):

        if component is None:
            return None

        if data_model is None:
            data_model_id = list(data_models)[0].id
            data_model = list(data_models)[0]
        else:
            data_model_id = data_model.id

        if isinstance(component, (Layer, Vertex, Edge, PEdge, Face, Volume, EdgeLoop)):
            if isinstance(component, Layer):
                geometry_model = component.Model.Model
            else:
                geometry_model = component.Layer.Model.Model
            cls = self.registered_geometry_classes[type(component)]
            return create_python_geometry(cls, component, data_model_id, self, geometry_model)

        if cls is None:
            c_slots = [x.Target.Key for x in component.Slots.Items]
            c_slot = list(set(c_slots) & set(self.registered_classes.keys()))
            if len(c_slot) == 0:
                if c_slots[0] not in self.registered_classes.keys():
                    self.register(c_slots[0], SimultanObject)
                    c_slot = [c_slots[0]]
            elif len(c_slot) > 1:
                num_superclasses = [len(self.registered_classes[x].__mro__) for x in c_slot]
                c_slot = [c_slot[num_superclasses.index(max(num_superclasses))]]
                # raise Warning(f'Component {component} has more than one registered taxonomy: {c_slot}')

            if c_slot[0] not in self.mapped_classes.keys():
                self.create_mapped_class(c_slot[0], self.registered_classes[c_slot[0]])

            cls = self.mapped_classes[c_slot[0]]

        if component is not None and component.Id in cls._cls_instances_dict.keys():
            return cls._cls_instances_dict[component.Id]
        else:
            return create_python_object(component,
                                        cls,
                                        data_model_id=data_model_id,
                                        object_mapper=self,
                                        data_model=data_model,

                                        *args,
                                        **kwargs)

    def get_typed_data_with_taxonomy(self, taxonomy: str, data_model=None, first=False):

        tax_components = data_model.find_components_with_taxonomy(taxonomy=taxonomy, first=first)
        return self.get_typed_data(component_list=tax_components)

    def get_properties(self, taxonomy):

        prop_dict = {}
        taxonomy_map = self.taxonomy_maps.get(taxonomy, None)

        if taxonomy_map is None:
            return prop_dict

        for prop in taxonomy_map.content:

            prop_dict[prop.property_name] = add_properties(prop_name=prop.property_name,
                                                           content=prop,
                                                           taxonomy_map=taxonomy_map,
                                                           taxonomy=taxonomy)

        return prop_dict

    def clear(self):
        for cls in self.mapped_classes.values():
            cls._cls_instances = WeakSet()


if config.default_mapper is None:
    config.default_mapper = PythonMapper()
