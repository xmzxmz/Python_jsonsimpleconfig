# -*- coding: utf-8 -*-
# * ********************************************************************* *
# *   Copyright (C) 2018 by xmz                                           *
# * ********************************************************************* *

__author__ = "Marcin Zelek (marcin.zelek@gmail.com)"
__copyright__ = "Copyright (C) xmz. All Rights Reserved."

################################################################################
# Import(s)                                                                    #
################################################################################

import json
import logging
import os
import sys

from .JscSection import JscSection


################################################################################
# Class                                                                        #
################################################################################

class JscData:
    """
    The JSC data container.
    """

    def __init__(self):
        self.__section = JscSection()
        self.__jsc = {}

    def __sectionFromJson(self, sectionData):
        if isinstance(sectionData, dict):
            keys = list(sectionData.keys())
            if not keys:
                self.__section.down()
            else:
                for key, value in sectionData.items():
                    if isinstance(value, dict):
                        self.__section.up(key)
                        self.__sectionFromJson(value)
                    else:
                        sectionName = self.__section.str()
                        if sectionName is None:
                            sectionName = JscSection.GLOBAL_SECTION_NAME

                        if sectionName not in self.__jsc:
                            self.__jsc[sectionName] = {}
                        self.__jsc[sectionName][key] = value

                    if key == keys[-1]:
                        self.__section.down()

    def addSectionData(self, sectionName, sectionData):
        """
        Put data for JSC tree section

        Parameters
        ----------
        sectionName : string
            Section name
        sectionData : dict
            Section data
        """
        if sectionName[0] == '[':
            sectionName = sectionName.lstrip('[')
        if sectionName[-1] == ']':
            sectionName = sectionName.rstrip(']')
        for key, value in sectionData.items():
            if sectionName not in self.__jsc:
                self.__jsc[sectionName] = {}
            self.__jsc[sectionName][key] = value

    def addSectionJsonString(self, sectionName, sectionJsonString):
        """
        Put data for JSC tree section using JSON format
        If JSON is correct will be added as JSC data branch

        Parameters
        ----------
        sectionName : string
            Section name
        sectionJsonString : string
            Section data as JSON string
        """
        try:
            sectionData = json.loads(sectionJsonString)
            self.addSectionData(sectionName, sectionData)

        except json.JSONDecodeError as e:
            logging.error(e.msg)
            logging.error(sys.exc_info())
            logging.error(sectionJsonString)
        except:
            logging.error(sys.exc_info())

    def getValue(self, sectionName, key, default=None) -> dict:
        """
        Get value for provided section and key
        For 'Global' variable section name should be None

        Parameters
        ----------
        sectionName : string
            Section name
        key : string
            Key name
        default : dict
            Default value if key does not exist

        Returns
        -------
        dict
            The value of the section key.
        """
        value = default
        sectionData = self.getSection(sectionName)
        if sectionData and key in sectionData:
            value = sectionData.get(key)
        return value

    def getSection(self, sectionName=None) -> dict:
        """
        Get full section branches

        Parameters
        ----------
        sectionName : string
            Section name

        Returns
        -------
        dict
            The section branch structure.
        """
        if sectionName is None or sectionName == '':
            sectionName = JscSection.GLOBAL_SECTION_NAME
        elif sectionName != JscSection.GLOBAL_SECTION_NAME:
            sectionName = sectionName.strip()
            if sectionName[0] != '"':
                sectionName = '"' + sectionName
            if sectionName[-1] != '"':
                sectionName = sectionName + '"'
        if sectionName in self.getSectionNames():
            return self.__jsc[sectionName]
        else:
            return None

    def getSectionNames(self):
        """
        Get all sections

        Returns
        -------
        dict
            Return list of the sections names or None if JSC is not defined.
        """
        if self.__jsc is not None:
            return self.__jsc.keys()
        else:
            return None

    def merge(self, jscData):
        """
        Merge another JSC data into current data

        Parameters
        ----------
        jscData : JscData
            JSC data from another source
        """
        if jscData is not None and isinstance(jscData, JscData):
            sectionNames = jscData.getSectionNames()
            if sectionNames is not None:
                for sectionName in sectionNames:
                    sectionData = jscData.getSection(sectionName)
                    if isinstance(sectionData, dict):
                        for key in sectionData:
                            value = sectionData.get(key)
                            if sectionName not in self.__jsc:
                                self.__jsc[sectionName] = {}
                            self.__jsc[sectionName][key] = value

    def str(self) -> str:
        """
        Get JSC data structure as string

        Returns
        -------
        string
            JSC data as string.
        """
        jscDataString = os.linesep
        sectionNames = self.getSectionNames()
        if sectionNames is not None:
            for sectionName in sectionNames:
                sectionPrint = "* Section"
                if sectionName == JscSection.GLOBAL_SECTION_NAME:
                    sectionPrint += " (Global):"
                else:
                    sectionPrint += " - {}:".format(sectionName)
                jscDataString += sectionPrint + os.linesep
                sectionData = self.getSection(sectionName)
                if isinstance(sectionData, dict):
                    for key in sectionData:
                        value = sectionData.get(key)
                        jscDataString += '*** [' + str(key) + '] : [' + str(value) + ']' + os.linesep

        return jscDataString

    def strHtml(self) -> str:
        """
        Get JSC data structure as string with new line as <br> for HTML format

        Returns
        -------
        string
            HTML format of JSC data.
        """
        return self.str().replace(os.linesep, '<br>' + os.linesep)

    def print(self):
        """
        Prints JSC string data
        """
        print(self.str())

    def printHtml(self):
        """
        Prints JSC data as HTML format
        """
        print(self.strHtml())

    def convertFromJson(self, jsonData):
        """
        Converts JSC data section from JSON

        Parameters
        ----------
        jsonData : dict
            JSON data to convert as dict
        """
        self.__sectionFromJson(jsonData)

    @staticmethod
    def fromJson(jsonData):
        """
        Get JSC data from JSON

        Parameters
        ----------
        jsonData : dict
            JSON data to convert as dict

        Returns
        -------
        string
            JSC data from provided JSON.
        """
        jscData = JscData()
        jscData.convertFromJson(jsonData)
        return jscData

################################################################################
#                                End of file                                   #
################################################################################
