# Pixel Bot by PixelAgent007

<div align="center"><p>
    <a href="https://github.com/PixelAgent007/pixelbot/pulse">
      <img alt="Last commit" src="https://img.shields.io/github/last-commit/PixelAgent007/pixelbot" />
    </a>
    <a href="https://github.com/PixelAgent007/pixelbot/blob/main/LICENSE">
      <img src="https://img.shields.io/github/license/PixelAgent007/pixelbot?style=flat-square&logo=GNU" alt="License"/>
    </a>
    <a href="https://wakatime.com/badge/github/PixelAgent007/pixelbot">
      <img src="https://wakatime.com/badge/github/PixelAgent007/pixelbot.svg"/>
    </a>
</div>

A simple discord bot built with [discord.py](https://discordpy.readthedocs.io/en/stable/) for QOL and Moderation purposes.
Also has some fun features, and was mainly built for the [Dark Moon SMP](https://discord.gg/eHAhkk2A5C).

## License

This Project is licensed under the GNU General Public License v3.0.
See [LICENSE](https://github.com/PixelAgent007/pixelbot/blob/main/LICENSE) for the full license or the header of [bot.py](https://github.com/PixelAgent007/pixelbot/blob/main/bot.py) for a shorter version.

## Requirements

+ Python => 3.10
+ Diverse pip packages (install by running):<br>
`python -m pip install -r requirements.txt`
+ ffmpeg
+ A mySQL / mariaDB server

## Note

The file **config/database.json** is required to run, but not included by default (for security reasons).
They have the following format:

### database.json

```json
{
    "DB": {
      "USER": "pixelbot",
      "DBNAME": "pixelbot",
      "HOST": "",
      "PASSWORD": "",
      "PORT": 3306
    }
}
```
