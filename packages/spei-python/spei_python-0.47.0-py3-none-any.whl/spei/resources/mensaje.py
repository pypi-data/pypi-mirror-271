from typing import Any, Optional

from lxml import etree
from pydantic import BaseModel, Extra

from spei.types import CategoriaOrdenPago


class Mensaje(BaseModel):
    categoria: Optional[CategoriaOrdenPago] = None
    ordenpago: Optional[Any] = None
    respuesta: Optional[Any] = None
    ensesion: Optional[Any] = None

    class Config:  # noqa: WPS306, WPS431
        extra = Extra.allow

    @classmethod
    def parse_xml(cls, mensaje):  # noqa: WPS210
        parser = etree.XMLParser(recover=True)
        mensaje = etree.fromstring(mensaje)  # noqa: S320
        body = mensaje.find(
            '{http://schemas.xmlsoap.org/soap/envelope/}Body',
        )
        ordenpago = body.find('{http://www.praxis.com.mx/}ordenpago')
        respuesta = body.find('{http://www.praxis.com.mx/}respuesta')

        if ordenpago is not None:
            element = etree.fromstring(  # noqa: S320
                bytes(ordenpago.text, encoding='cp850'),
                parser,
            )
            categoria = element.attrib['categoria']

            if categoria == CategoriaOrdenPago.ensesion:
                return cls(
                    categoria=categoria, ensesion=element,
                )

            return cls(categoria=categoria, ordenpago=element)

        if respuesta is not None:
            element = etree.fromstring(  # noqa: S320
                bytes(respuesta.text, encoding='cp850'),
            )
            categoria = element.attrib['categoria']
            return cls(categoria=categoria, respuesta=element)

        raise NotImplementedError
