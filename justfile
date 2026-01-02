default:
  uv run main.py

test:
  uv run main.py "https://www.youtube.com/watch?v=nlh9p0a2-jE"
  # uv run main.py "https://www.youtube.com/watch?v=FOq-Ygl2q0U"
  # uv run main.py "https://www.youtube.com/watch?v=MTb_8T5d2SI"
  # uv run main.py "https://www.youtube.com/watch?v=zJKPdzDdzUQ"
  # uv run main.py "https://www.youtube.com/watch?v=UntGhIIwN1g"
  #
  # uv run main.py "https://www.youtube.com/watch?v=M56Q6ejz7CI"

test-bad:
  uv run main.py "https://www.yout.com/w?v=M56Q6ejz7CI"

srv:
  uv run main.py --srv

test-web:
  curl.exe -XPOST http://localhost:9000 -d '{"entry": {"url": "https://www.youtube.com/watch?v=UntGhIIwN1g"}}'
  curl.exe -XPOST http://localhost:9000 -d '{"entry": {"url": "https://www.youtube.com/watch?v=nlh9p0a2-jE"}}'
  curl.exe -XPOST http://localhost:9000 -d '{"entry": {"url": "https://www.youtube.com/watch?v=FOq-Ygl2q0U"}}'
  curl.exe -XPOST http://localhost:9000 -d '{"entry": {"url": "https://www.youtube.com/watch?v=MTb_8T5d2SI"}}'
  curl.exe -XPOST http://localhost:9000 -d '{"entry": {"url": "https://www.youtube.com/watch?v=zJKPdzDdzUQ"}}'
  curl.exe -XPOST http://localhost:9000 -d '{"entry": {"url": "https://www.youtube.com/watch?v=UntGhIIwN1g"}}'
  curl.exe -XPOST http://localhost:9000 -d '{"entry": {"url": "https://www.youtube.com/watch?v=M56Q6ejz7CI"}}'

clean:
  -rm -fr out
  -rm *.mp3
  -rm *.webp
