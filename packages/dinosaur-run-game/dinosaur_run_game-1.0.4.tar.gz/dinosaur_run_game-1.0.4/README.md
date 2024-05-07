# speech_recognition

## Prerequisite
-   ```shell
    brew install portaudio
    pip install setuptools
    pip install pyaudio
    pip install google-cloud-speech
    ```
    

## How to publish the game to PyPI

- ```shell
  python setup.py sdist
  twine upload dist/*
  ```

## How to install the game
- ```shell
  pipx install nongped-rungame
  nongped-rungame
  ```

## Useful Links

- music: https://mixkit.co/free-sound-effects/desert/