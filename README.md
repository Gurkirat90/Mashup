# YouTube Singer Mashup Generator
A Python application that automatically creates a mashup of songs from a given singer by downloading YouTube audio, trimming each track, merging them, and delivering the final mashup file.
The project includes:
- CLI version (command line)
- Web version using Flask
- Email delivery of mashup
---
## USAGE
```bash
python program.py <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>
```
### Example
```bash
python program.py "Chemma Y" 15 30 mashup.mp3
```
---

## Parameters
| Parameter        | Description                                                   |
|------------------|---------------------------------------------------------------|
| `SingerName`     | Name of the singer whose songs will be used for the mashup   |
| `NumberOfVideos` | Number of YouTube videos to fetch (must be greater than 10)  |
| `AudioDuration`  | Duration of each audio clip in seconds (must be > 20)        |
| `OutputFileName` | Name of the final generated mashup audio file                |

---

## Output
```
Mashup created successfully: mashup.mp3
```
---
### Requirements
- Python 3.8+
- FFmpeg installed
- Internet connection
- Gmail account (for email sending)
### Limitations
- Depends on YouTube search results
- Audio quality depends on source video
- Email attachment size limits may apply
---
