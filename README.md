# Authoring Content

Make changes to the content in the chapters directory.

To test
```
./runLocal.sh
```
And navigate on a browser to http://localhost:8000/

To recompile after you make changes
```
python compile.py
```

Never directly modify files in the en directory

# Development

Download dependencies
```
pip3 install -r requirements.txt
```

# Using a Virtual Environment
You can optionally use a virtual environment.

Create virtual environment
```
python3 -m venv .venv
```

Enter virtual environment
```
source .venv/bin/activate
```

You should run `source .venv/bin/activate` everytime you start working from a new terminal session
