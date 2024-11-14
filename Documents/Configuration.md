# Configuration

All your configurations will be in a file in the root directory, called `config.json`, which is a copy of `config.example.json`. You can change the values in `config.json` to your liking.

## Values

- `verbose`: `boolean` - If `true`, the application will print out more information.
- `profile_profile`: `string` - The path to your bowser profile. This is used to use your Social Media Accounts without having to log in every time you run the application.
- `headless`: `boolean` - If `true`, the application will run in headless mode. This means that the browser will not be visible.
- `llm`: This will decide the Large Language Model MPV2 uses to generate tweets, scripts, image prompts and more. If left empty, the default model (`gpt35_turbo`) will be used. Here are your choices:
- `image_prompt_llm`: `string` - The Large Language Model that will be used to generate image prompts. If left empty, the default model (`gpt35_turbo`) will be used. Here are your choices:`
    * `gpt4`
    * `gpt35_turbo`
    * `llama2_7b`
    * `google`
    * `llama2_70b`
    * `mixtral_8x7b`

- `language`: `string` - The language that will be used to generate & post tweets.
- `image_model`: `string` - What AI Model you want to use to generate images, here are your choices:
    * `v1`
    * `v2`
    * `v3` (DALL-E)
    * `lexica`
    * `simurg`
    * `animefy`
    * `raava`
    * `shonin`
- `threads`: `number` - The amount of threads that will be used to execute operations, e.g. writing to a file using MoviePy.
- `is_for_kids`: `boolean` - If `true`, the application will upload the video to YouTube Shorts as a video for kids.
- `assembly_ai_api_key`: `string` - Your Assembly AI API key. Get yours from [here](https://www.assemblyai.com/app/).
- `font`: `string` - The font that will be used to generate images. This should be a `.ttf` file in the `fonts/` directory.
- `imagemagick_path`: `string` - The path to the ImageMagick binary. This is used by MoviePy to manipulate images. Install ImageMagick from [here](https://imagemagick.org/script/download.php) and set the path to the `magick.exe` on Windows, or on Linux/MacOS the path to `convert` (usually /usr/bin/convert).

## Example

```json
{
  "verbose": true,
  "browser": "firefox",
  "headless": true,
  "profile_path": "",
  "language": "English",
  "llm": "Gemini",
  "image_prompt_llm": "Gemini",
  "image_gen": "hercai",
  "image_model": "shonin",
  "tts_engine": "local_tts",
  "tts_voice": "nova",
  "threads": 8,
  "is_for_kids": false,
  "zip_url": "https://huggingface.co/AZILS/BG/resolve/main/BG.zip?download=true",
  "local_tts_url": "https://imseldrith-tts-openai-free.hf.space/v1/audio/speech",
  "gemini_api_key": "AIzaSyC6N1MVe9WmAFjWMNuXjlaLnYa8eO813tY",
  "assembly_ai_api_key": "e9c253a938184370becdf77f2a9e6a45",
  "elevenlabs_api_key": "bfd724a75fef2b01b2347d3dcfe10079f816976a32121",
  "openai_api_key": "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",
  "stability_api_key": "abfd724a75fef2b01b2347d3dcfe10079f816976a32121",
  "segmind_api_key": "bfd724a75fef2b01b2347d3dcfe10079f816976a32121",
  "font": "bold_font.ttf",
  "imagemagick_path": "/usr/bin/convert"
}

```
