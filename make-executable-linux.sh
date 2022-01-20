#!/bin/bash
pyinstaller --log-level ERROR --clean -y --distpath .build/dist/linux --workpath .build/tmp --onefile pydyna.spec
