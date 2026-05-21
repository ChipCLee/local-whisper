# Local Whisper API

FastAPI wrapper around `faster-whisper` with OpenAI-compatible transcription endpoints.

## Docker

Build the image:

```sh
docker build -t local-whisper .
```

Run the API on port 9000:

```sh
docker run --rm -p 9000:9000 local-whisper
```

The first run downloads the configured Whisper model into the container. To keep the model cache between runs:

```sh
docker run --rm -p 9000:9000 -v local-whisper-models:/models local-whisper
```

Override model settings with environment variables:

```sh
docker run --rm -p 9000:9000 \
  -e WHISPER_MODEL=small \
  -e WHISPER_DEVICE=cpu \
  -e WHISPER_COMPUTE_TYPE=int8 \
  local-whisper
```
