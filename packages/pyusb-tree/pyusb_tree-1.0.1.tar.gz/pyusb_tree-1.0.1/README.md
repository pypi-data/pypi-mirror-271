# pyusb-tree

Python package to parse USB Device Tree Viewer (https://www.uwe-sieber.de/usbtreeview_e.html) output to pydantic.

## Limitations

- Only supports windows
- Extracting data from USB Device Tree Viewer is slow

## Installation

You can install the package via pip:

```
pip install pyusb-tree
```

## Usage

```python
from pyusb_tree import get_devices

data = get_devices()
```

## Output

```py
Node(
    name="JOHN-PC",
    attributes={...},
    children=[
        Node(
            name="Intel(R) USB 3.0 eXtensible Host Controller",
            attributes={...},
            children=[
                Node(
                    name="USB Root Hub (USB 3.0)",
                    attributes={...},
                    children=[
                        Node(
                            name="[Port1]",
                            attributes={...},
                            children=[],
                        ),
                        Node(
                            name="[Port2]",
                            attributes={...},
                            children=[],
                        ),
                        Node(
                            name="[Port3]",
                            attributes={...},
                            children=[],
                        ),
                    ],
                ),
            ],
        ),
    ],
)
```

## License

This project is licensed under the terms of the MIT license.
