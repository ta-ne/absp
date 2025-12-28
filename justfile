default:
  uv run main.py

# test: clean
test:
  uv run main.py "https://www.youtube.com/watch?v=nlh9p0a2-jE"
  uv run main.py "https://www.youtube.com/watch?v=FOq-Ygl2q0U"
  uv run main.py "https://www.youtube.com/watch?v=MTb_8T5d2SI"
  uv run main.py "https://www.youtube.com/watch?v=zJKPdzDdzUQ"
  uv run main.py "https://www.youtube.com/watch?v=UntGhIIwN1g"

  uv run main.py "https://www.youtube.com/watch?v=M56Q6ejz7CI"

clean:
  -rm -fr out
  -rm *.mp3
  -rm *.webp
