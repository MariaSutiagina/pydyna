#!/bin/bash
pyinstaller --log-level ERROR --clean -y --distpath .build/dist/windows --workpath .build/tmp --onefile pydyna.spec
