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
