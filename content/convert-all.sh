#!/bin/bash
find . -type f -name "*.png" | while read f; do
    convert "$f" "${f%.png}.jpg" && rm "$f"
done

