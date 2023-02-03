import os


def generate_html(api, current_api_name):
    return """
            <html>
              <head>
                <title>Smart-Plug</title>
                <style>
                    .container {{
                        margin-left: auto;
                        margin-right: auto;
                        width: 24em;
                        display: flex;
                    }}
                    input, select {{
                        width: 12em;
                    }}
                </style>
              </head>
              <body>
                <div class="container">
                    <h>API Selection<h/>
                    <form method="post">
                        <select name="api" id="api">{}</select>
                        <input type="submit" value="Set API">
                    </form>
                    <h>{} Settings<h>
                    {}
                <div/>
              </body>
            </html>""".format(
        __get_api_html_options(current_api_name),
        current_api_name,
        api.get_html_options(),
    )


def __get_api_html_options(current_api_name):
    api_options = []
    for file in os.ilistdir("/api/implementations/"):
        if (file[1] == 0x4000) and (file[0] != "template_api"):
            api_options.append(file[0])
    html_options = ""
    for option in api_options:
        html_options = html_options + __get_api_html_name(option, current_api_name)
    return html_options


def __get_api_html_name(name, current_api_name):
    selected_placeholder = ""
    if name == current_api_name:
        selected_placeholder = """selected="selected" """
    return """<option {} value="{}">{}</option>""".format(
        selected_placeholder, name, name
    )
