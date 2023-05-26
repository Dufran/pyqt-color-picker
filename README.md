# Color Picker

Simple pyqt6 app that works as color picker

## Goal

- Create a app window with 2 fields
  - Field 1: Color of pixel where cursor is located
    - Pool color of pixel with signal
  - Field 2: Color of pixel where last click event happen
- App should be always on top

## Packaging

For creation of executable file we will use pyintaller. It allows to build executable app for multiple platforms.

It's recommended to use pyenv for python version handling, and it require some extra argument when installing

```bash
PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 3.11.0
```

## Summary

Pros and cons when creating apps with pyqt6

Pros:

- Allow you to quickly create app using python
- Full QT syntax

Cons:

- Need to use qt-designer for creation .ui file even for small apps
-

## Comparison with Electron app
