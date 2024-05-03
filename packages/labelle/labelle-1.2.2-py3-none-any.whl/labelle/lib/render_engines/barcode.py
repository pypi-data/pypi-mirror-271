from __future__ import annotations

import barcode as barcode_module
from PIL import Image

from labelle.lib.barcode_writer import BarcodeImageWriter
from labelle.lib.constants import DEFAULT_BARCODE_TYPE, BarcodeType
from labelle.lib.render_engines.render_context import RenderContext
from labelle.lib.render_engines.render_engine import (
    RenderEngine,
    RenderEngineException,
)

if DEFAULT_BARCODE_TYPE != BarcodeType.CODE128:
    # Ensure that we fail fast if the default barcode type is adjusted
    # and the code below hasn't been updated.
    raise RuntimeError(
        "The conditional below assumes that the default barcode type is CODE128. "
        "Different barcodes have different quirks, so we should manually test the "
        "new default to ensure a good user experience in the GUI when the initial "
        "value is an empty string."
    )


class BarcodeRenderError(RenderEngineException):
    def __init__(self) -> None:
        msg = "Barcode render error"
        super().__init__(msg)


class BarcodeRenderEngine(RenderEngine):
    def __init__(self, content: str, barcode_type: str | None) -> None:
        super().__init__()
        self.content = content
        self.barcode_type = barcode_type or DEFAULT_BARCODE_TYPE

    def render(self, context: RenderContext) -> Image.Image:
        if (
            self.barcode_type == DEFAULT_BARCODE_TYPE == BarcodeType.CODE128
            and self.content == ""
        ):
            # An exception is raised on the empty string. Since this is
            # the default code, we really don't want to trigger a popup
            # in the GUI before the user entered a barcode.
            self.content = " "
        try:
            code = barcode_module.get(
                self.barcode_type, self.content, writer=BarcodeImageWriter()
            )
            bitmap = code.render(
                {
                    "font_size": 0,
                    "vertical_margin": 8,
                    "module_height": context.height_px - 16,
                    "module_width": 2,
                    "background": "black",
                    "foreground": "white",
                }
            )
        except BaseException as e:
            raise BarcodeRenderError from e
        return bitmap
