# Setup

Download dependencies
```
python -m pip install -r requirements.txt
```

# Editing Content

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

Warning: Never directly modify files in the en directory


# Adding new Chapters / Examples

The book outline is defined in the file bookOutline.hjson. If you want to create a new chapter or a new worked example put it in there. Then run compile and you will see a skeleton directory created in chapters.

# Submit a pull request

https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request

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
