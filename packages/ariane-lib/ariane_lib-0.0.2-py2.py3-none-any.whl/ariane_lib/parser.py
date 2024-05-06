#!/usr/bin/env python

import hashlib
import xmltodict
import json

from pathlib import Path
from zipfile import ZipFile

from ariane_lib.key_map import KeyMapCls
from ariane_lib.key_map import KeyMapMeta
from ariane_lib.key_map import OptionalArgList
from ariane_lib.section import SurveySection
from ariane_lib.shot import SurveyShot
from ariane_lib.types import ArianeFileType

from functools import cached_property


def _extract_zip(input_zip):
    input_zip=ZipFile(input_zip)
    return {name: input_zip.read(name) for name in input_zip.namelist()}


class ArianeParser(object, metaclass=KeyMapMeta):

    _KEY_MAP = KeyMapCls({
        "constraints": ["Constraints"],
        "cartoEllipse": ["CartoEllipse"],
        "cartoLine": ["CartoLine"],
        "cartoLinkedSurface": ["CartoLinkedSurface"],
        "cartoOverlay": ["CartoOverlay"],
        "cartoPage": ["CartoPage"],
        "cartoRectangle": ["CartoRectangle"],
        "cartoSelection": ["CartoSelection"],
        "cartoSpline": ["CartoSpline"],
        "firstStartAbsoluteElevation": ["firstStartAbsoluteElevation"],
        "geoCoding": OptionalArgList(["geoCoding"]),
        "name": ["caveName"],
        "layers": ["Layers"],
        "listAnnotation": ["ListAnnotation"],
        "unit": ["unit"],
        "useMagneticAzimuth": ["useMagneticAzimuth"],
        "_cavefile": ["CaveFile"],
        "_shots_list": ["Data"],
        "_shots": ["SurveyData", "SRVD"]
    })

    def __init__(self, filepath: str, pre_cache : bool = True) -> None:

        self._filepath = Path(filepath)

        if not self.filepath.is_file():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        if pre_cache:
            _ = self.data

        else:
            # Ensure at least that the file type is valid
            _ = self.filetype
        
    def __repr__(self) -> str:
        repr = f"[ArianeSurveyFile {self.filetype.name}] `{self.filepath}`:"
        for key in self._KEY_MAP.keys():
            if key.startswith("_"):
                continue
            repr += f"\n\t- {key}: {getattr(self, key)}"
        repr += f"\n\t- shots: Total Shots: {len(self.shots)}"
        repr += f"\n\t- hash: {self.hash}"
        return repr
    
    def _as_binary(self):
        with open(self.filepath, "rb") as f:
            return f.read()
        
    # Hash related methods
    
    @cached_property
    def __hash__(self):
        return hashlib.sha256(self._as_binary()).hexdigest()
    
    @property
    def hash(self):
        return self.__hash__
    
    # File Timestamps

    @property
    def lstat(self):
        return self.filepath.lstat()

    @property
    def date_created(self):
        return self.lstat.st_ctime
    
    @property
    def date_last_modified(self):
        return self.lstat.st_mtime
    
    @property
    def date_last_opened(self):
        return self.lstat.st_atime
    
    # Loading & Reading the XML File
    
    @cached_property
    def _data(self):

        if self.filetype == ArianeFileType.TML:
            xml_data = _extract_zip(self.filepath)["Data.xml"]

        elif self.filetype == ArianeFileType.TMLU:
            with open(self.filepath, "r") as f:
                xml_data = f.read()

        else:
            raise ValueError(f"Unknown file format: {self.filetype}")
        
        return xmltodict.parse(xml_data)
    
    # Export Formats

    def to_json(self):
        return json.dumps(self.data, indent=4, sort_keys=True)
    
    # =============== Descriptive Properties =============== #

    @property
    def data(self):
        return self._KEY_MAP.fetch(self._data, "_cavefile")

    @property
    def filepath(self):
        return self._filepath

    @property
    def filetype(self):
        try:
            return ArianeFileType.from_str(self.filepath.suffix[1:])
        except ValueError as e:
            raise TypeError(e) from e
    
    @cached_property
    def shots(self):
        return [
            SurveyShot(data=survey_shot)
            for survey_shot in self._KEY_MAP.fetch(self._shots_list, "_shots")
        ]
    
    @cached_property
    def sections(self):
        section_map = dict()
        for shot in self.shots:
            try:
                section_map[shot.section].add_shot(shot)
            except KeyError:
                section_map[shot.section] = SurveySection(shot=shot)
        return list(section_map.values())
    