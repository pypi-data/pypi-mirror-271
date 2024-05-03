# Grid - A Gradio Custom Component
# Created by Daniel Ialcin Misser Westergaard
# https://huggingface.co/dwancin
# (c) 2024

from __future__ import annotations

from typing import Literal

from gradio_client.documentation import document

from gradio.blocks import BlockContext
from gradio.component_meta import ComponentMeta


class Grid(BlockContext, metaclass=ComponentMeta):
    """
    Grid is a layout element within Blocks that renders all children in a two-dimensional grid system.
    Example:
        with gr.Blocks() as demo:
            with Grid(columns=3):
                gr.Image("lion.jpg", scale=2)
                gr.Image("tiger.jpg", scale=1)
                gr.Image("leopard.jpg", scale=1)
        demo.launch()
    Guides: controlling-layout
    """

    EVENTS = []

    def __init__(
        self,
        *,
        variant: Literal["default", "panel"] = "default",
        visible: bool = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        columns: int = 3
    ):
        """
        Parameters:
            variant: Grid type, 'default' (no background) or 'panel' (gray background color and rounded corners).
            visible: If False, the grid will be hidden.
            elem_id: An optional string that is assigned as the id of this element in the HTML DOM. Can be used for targeting CSS styles.
            elem_classes: An optional string or list of strings that are assigned as the class of this element in the HTML DOM. Can be used for targeting CSS styles.
            render: If False, this layout will not be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.
            columns: Defines the number of columns in the grid.
        """
        
        self.variant = variant
        self.columns = columns
        
        BlockContext.__init__(
            self,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            render=render,
        )

    @staticmethod
    def update(
        visible: bool | None = None,
    ):
        return {
            "visible": visible,
            "__type__": "update",
        }
