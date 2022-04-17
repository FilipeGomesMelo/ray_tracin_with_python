# Ray Tracing in Python

> Project from IF680 (PROCESSAMENTO GRÁFICO)

Recommended that you run using pypy3 interpreter and not CPython for better rendering times

## Using on Windows using chocolatey
1. Install the [chocolatey](https://chocolatey.org/install)
2. Run the following command:
```bash
choco install pypy3
pypy3 main.py
```

## Running the project
There are two arguments that can be passed to the program:
- jsonpath: The path of the json file with the scene description
- imageout: The path of the image to be saved

Eg: If you want to load the inputs/japao.json and save the output to image.ppm
```bash
pypy3 main.py inputs/japao.json image.ppm
```

![Sample image](./Sample.png)