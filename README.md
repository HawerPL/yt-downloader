# YT downloader

Simple desktop app to download audio or video from YouTube. 

## Description

The app allows a public YouTube video to be downloaded in the format of your choice based on the URL provided. 

The UI supports changing the language and theme of the application.

## Getting Started

* To clone repository and install required libs use commands:
```
  git clone https://github.com/HawerPL/yt-downloader.git
  cd yt-downloader
  pip install -r requirements.txt
```
### Executing program

* To run program use command:
```
  python main.py
```

## Help

### Description for settings
| Settings | Default Value | Available values                      | Description                |
|----------| ----------- |---------------------------------------|----------------------------|
| LANGUAGE | EN | EN, PL                                | Language for app           |
| MODE     | System | System, Light, Dark                   | Default theme for app      |
| GEOMETRY     | "1020x720" | Any value in format %Number%x%Number% | Default windows resolution |

### Add new language

* For example deutsch in Linux
```
  cd translations
  mkdir -p de/LC_MESSAGES
  cp en/LC_MESSAGES/messages.po de/LC_MESSAGES/messages.po
  vi de/LC_MESSAGES/messages.po
  cd ..
  pybabel compile -f -d translations
```

* For example deutsch in Windows
```
  Set-Location translations
  New-Item -ItemType Directory -Path .\de\LC_MESSAGES -Force
  Copy-Item .\en\LC_MESSAGES\messages.po .\de\LC_MESSAGES\messages.po
  notepad .\de\LC_MESSAGES\messages.po
  Set-Location ..
  pybabel compile -f -d translations
```

## Authors

Contributors names and contact info
* HawerPL

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments
* [ctkinter](https://github.com/topics/ctkinter)