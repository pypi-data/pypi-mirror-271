
import gradio as gr
from app import demo as app
import os

_docs = {'Grid': {'description': 'Grid is a layout element within Blocks that renders all children in a two-dimensional grid system.\n    with gr.Blocks() as demo:\n        with Grid(columns=3):\n            gr.Image("lion.jpg", scale=2)\n            gr.Image("tiger.jpg", scale=1)\n            gr.Image("leopard.jpg", scale=1)\n    demo.launch()', 'members': {'__init__': {'variant': {'type': '"default" | "panel"', 'default': '"default"', 'description': "Grid type, 'default' (no background) or 'panel' (gray background color and rounded corners)."}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'If False, the grid will be hidden.'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string that is assigned as the id of this element in the HTML DOM. Can be used for targeting CSS styles.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional string or list of strings that are assigned as the class of this element in the HTML DOM. Can be used for targeting CSS styles.'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'If False, this layout will not be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.'}, 'columns': {'type': 'int', 'default': '3', 'description': 'Defines the number of columns in the grid.'}}, 'postprocess': {}}, 'events': {}}, '__meta__': {'additional_interfaces': {}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_grid`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%201.0.0%20-%20orange">  
</div>

Grid is a layout element within Blocks that renders all children in a two dimensional grid system.
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_grid
```

## Usage

```python
import gradio as gr
from gradio_grid import Grid


with gr.Blocks() as demo:
    gr.Markdown("# Demo")
    gr.Markdown("This demo showcases the `Grid` layout element within Gradio Blocks. Below, the same concept is depicted using the existing layout elements for comparison.")
    gr.Markdown("---\n## Grid")
    with Grid():
            gr.Textbox(label="input1", interactive=True)
            gr.Textbox(label="input2", interactive=True)
            gr.Textbox(label="input3", interactive=True)
            gr.Textbox(label="input4", interactive=True)
            gr.Textbox(label="input5", interactive=True)
            gr.Textbox(label="input6", interactive=True)
    gr.Markdown("---\n## Row")
    with gr.Row():
            gr.Textbox(label="input1", interactive=True)
            gr.Textbox(label="input2", interactive=True)
            gr.Textbox(label="input3", interactive=True)
            gr.Textbox(label="input4", interactive=True)
            gr.Textbox(label="input5", interactive=True)
            gr.Textbox(label="input6", interactive=True)
    gr.Markdown("---\n## Column")
    with gr.Column():
            gr.Textbox(label="input1", interactive=True)
            gr.Textbox(label="input2", interactive=True)
            gr.Textbox(label="input3", interactive=True)
            gr.Textbox(label="input4", interactive=True)
            gr.Textbox(label="input5", interactive=True)
            gr.Textbox(label="input6", interactive=True)
    gr.Markdown("---")

if __name__ == "__main__":
    demo.launch()

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `Grid`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["Grid"]["members"]["__init__"], linkify=[])







    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {};
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
