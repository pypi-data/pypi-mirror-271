# `gradio_grid`
<div style="display: flex; gap: 7px;">
  <a href="https://pypi.org/project/gradio-grid/" target="_blank"><img alt="PyPI" src="https://img.shields.io/pypi/v/gradio-grid"></a>
  <a href="https://huggingface.co/spaces/dwancin/gradio_grid" target="_blank"><img alt="Demo" src="https://img.shields.io/badge/%F0%9F%A4%97%20Demo-%23097EFF?style=flat&logoColor=black"></a>
  <a href="https://github.com/dwancin/gradio-grid" target="_blank"><img alt="Static Badge" src="https://img.shields.io/badge/Repository-white?logo=github&logoColor=black"></a>
</div>

Grid is a layout element within Blocks that renders all children in a two dimensional grid system.

## Installation

```bash
pip install gradio_grid
```

## Usage Example

```python
import gradio as gr
from gradio_grid import Grid

with gr.Blocks() as demo:
    with Grid():
        gr.Textbox(label="input1", interactive=True)
        gr.Textbox(label="input2", interactive=True)
        gr.Textbox(label="input3", interactive=True)
        gr.Textbox(label="input4", interactive=True)
        gr.Textbox(label="input5", interactive=True)
        gr.Textbox(label="input6", interactive=True)

demo.launch()
```

### Initialization

<table>
<thead>
<tr>
<th align="left">name</th>
<th align="left" style="width: 25%;">type</th>
<th align="left">default</th>
<th align="left">description</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><code>variant</code></td>
<td align="left" style="width: 25%;">

```python
"default" | "panel"
```

</td>
<td align="left"><code>"default"</code></td>
<td align="left">Grid type, 'default' (no background) or 'panel' (gray background color and rounded corners).</td>
</tr>

<tr>
<td align="left"><code>visible</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If False, the grid will be hidden.</td>
</tr>

<tr>
<td align="left"><code>elem_id</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">An optional string that is assigned as the id of this element in the HTML DOM. Can be used for targeting CSS styles.</td>
</tr>

<tr>
<td align="left"><code>elem_classes</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">An optional string or list of strings that are assigned as the class of this element in the HTML DOM. Can be used for targeting CSS styles.</td>
</tr>

<tr>
<td align="left"><code>render</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If False, this layout will not be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.</td>
</tr>

<tr>
<td align="left"><code>columns</code></td>
<td align="left" style="width: 25%;">

```python
int
```

</td>
<td align="left"><code>3</code></td>
<td align="left">Defines the number of columns in the grid.</td>
</tr>
</tbody></table>
