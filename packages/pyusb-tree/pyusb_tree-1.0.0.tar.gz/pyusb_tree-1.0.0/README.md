# pyusb-tree

Python package to parse USB Device Tree Viewer (https://www.uwe-sieber.de/usbtreeview_e.html) output to pydantic.

## Installation

You can install the package via pip:

```
pip install pyusb-tree
```

## Usage

1. Extract the data from `UsbTreeView.exe`, manually or via code.
   ```
   UsbTreeView.exe -X=usb.xml
   ```
2. Convert xml data to pydantic format.

   ```python
   import json

   from pyusb_tree import extract_xml

   data = extract_xml("usb.xml")

   # preety print
   print(json.dumps(data.model_dump(), indent=2))
   ```

## Ouput

```json
{
  "name": "JOHN-PC",
  "attributes": {...},
  "children": [
    {
      "name": "Intel(R) USB 3.0 eXtensible Host Controller - 1.0 (Microsoft) - USB xHCI Compliant Host Controller",
      "attributes": {...},
      "children": [
        {
          "name": "USB Root Hub (USB 3.0)",
          "attributes": {...},
          "children": [
            {
              "name": "[Port1]",
              "attributes": {...},
              "children": []
            },
            {
              "name": "[Port2]",
              "attributes": {...},
              "children": []
            },
            {
              "name": "[Port3]",
              "attributes": {...},
              "children": []
            },
            {
              "name": "[Port4] : Sunplus Innovation USB Composite Device - Integrated Webcam - Camera",
              "attributes": {...},
              "children": [
                {
                  "name": "Integrated Webcam - USB Video Device",
                  "attributes": {...},
                  "children": []
                }
              ]
            },
            {
              "name": "[Port5] : Intel Intel(R) Wireless Bluetooth(R) - 10\u00d7 Bluetooth, 2\u00d7 Media, 2\u00d7 Audio, Net",
              "attributes": {...},
              "children": [
                {
                  "name": "Bluetooth Device (RFCOMM Protocol TDI)",
                  "attributes": {...},
                  "children": []
                },
                {
                  "name": "Microsoft Bluetooth Enumerator",
                  "attributes": {...},
                  "children": [
                    {
                      "name": "AirPods - Microsoft Bluetooth A2dp Source",
                      "attributes": {...},
                      "children": []
                    },
                    {
                      "name": "WOLF THUNDER - Microsoft Bluetooth A2dp Source",
                      "attributes": {...},
                      "children": []
                    },
                    {
                      "name": "AirPods Avrcp Transport - Microsoft Bluetooth Avrcp Transport Driver",
                      "attributes": {...},
                      "children": []
                    },
                    {
                      "name": "WOLF THUNDER Avrcp Transport - Microsoft Bluetooth Avrcp Transport Driver",
                      "attributes": {...},
                      "children": []
                    },
                    {
                      "name": "AirPods Avrcp Transport - Microsoft Bluetooth Avrcp Transport Driver",
                      "attributes": {...},
                      "children": []
                    },
                    {
                      "name": "WOLF THUNDER Avrcp Transport - Microsoft Bluetooth Avrcp Transport Driver",
                      "attributes": {...},
                      "children": []
                    },
                    {
                      "name": "AirPods Hands-Free AG - Microsoft Bluetooth Hands-Free Profile AudioGateway role",
                      "attributes": {...},
                      "children": [
                        {
                          "name": "AirPods Hands-Free - Microsoft Bluetooth Hands-Free Audio device",
                          "attributes": {...},
                          "children": []
                        }
                      ]
                    },
                    {
                      "name": "WOLF THUNDER Hands-Free AG - Microsoft Bluetooth Hands-Free Profile AudioGateway role",
                      "attributes": {...},
                      "children": [
                        {
                          "name": "WOLF THUNDER Hands-Free - Microsoft Bluetooth Hands-Free Audio device",
                          "attributes": {...},
                          "children": []
                        }
                      ]
                    },
                    {
                      "name": "AAP Server",
                      "attributes": {...},
                      "children": []
                    },
                    {
                      "name": "AirPods - Bluetooth Device",
                      "attributes": {...},
                      "children": []
                    },
                    {
                      "name": "WOLF THUNDER - Bluetooth Device",
                      "attributes": {...},
                      "children": []
                    }
                  ]
                },
                {
                  "name": "Bluetooth Device (Personal Area Network)",
                  "attributes": {...},
                  "children": []
                },
                {
                  "name": "Microsoft Bluetooth LE Enumerator",
                  "attributes": {...},
                  "children": []
                }
              ]
            },
            {
              "name": "[Port6]",
              "attributes": {...},
              "children": []
            },
            {
              "name": "[Port7]",
              "attributes": {...},
              "children": []
            },
            {
              "name": "[Port8]",
              "attributes": {...},
              "children": []
            },
            {
              "name": "[Port9]",
              "attributes": {...},
              "children": []
            },
            {
              "name": "[Port10]",
              "attributes": {...},
              "children": []
            },
            {
              "name": "[Port11]",
              "attributes": {...},
              "children": []
            },
            {
              "name": "[Port12]",
              "attributes": {...},
              "children": []
            },
            {
              "name": "[Port13]",
              "attributes": {...},
              "children": []
            },
            {
              "name": "[Port14]",
              "attributes": {...},
              "children": []
            },
            {
              "name": "[Port15]",
              "attributes": {...},
              "children": []
            },
            {
              "name": "[Port16]",
              "attributes": {...},
              "children": []
            },
            {
              "name": "[Port17]",
              "attributes": {...},
              "children": []
            },
            {
              "name": "[Port18]",
              "attributes": {...},
              "children": []
            },
            {
              "name": "[Port19]",
              "attributes": {...},
              "children": []
            },
            {
              "name": "[Port20]",
              "attributes": {...},
              "children": []
            },
            {
              "name": "[Port21]",
              "attributes": {...},
              "children": []
            },
            {
              "name": "[Port22]",
              "attributes": {...},
              "children": []
            },
            {
              "name": "[Port23]",
              "attributes": {...},
              "children": []
            },
            {
              "name": "[Port24]",
              "attributes": {...},
              "children": []
            }
          ]
        }
      ]
    }
  ]
}
```

## License

This project is licensed under the terms of the MIT license.
