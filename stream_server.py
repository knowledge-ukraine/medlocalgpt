import os
# os.environ["OPENAI_API_KEY"] = ""

from flask import Flask, Response
import threading
import queue

from langchain.llms import OpenAI
# from langchain.callbacks.base import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

app = Flask(__name__)

@app.route('/')
def index():
    return Response('''
<!DOCTYPE html>
<html>
<head><title>Flask Streaming Langchain Example</title></head>
<body>
    <div id="output"></div>
    <script>
        const outputEl = document.getElementById('output');
        (async function() {  // wrap in async function to use await
            try {
                const response = await fetch('/chain', {method: 'POST'});
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                while (true) {
                    const { done, value } = await reader.read();
                    if (done) { break; }
                    const decoded = decoder.decode(value, {stream: true});
                    outputEl.innerText += decoded;
                }
            } catch (err) {
                console.error(err);
            }
        })();
    </script>
</body>
</html>
''', mimetype='text/html')

class ThreadedGenerator:
    def __init__(self):
        self.queue = queue.Queue()

    def __iter__(self):
        return self

    def __next__(self):
        item = self.queue.get()
        if item is StopIteration: raise item
        return item

    def send(self, data):
        self.queue.put(data)

    def close(self):
        self.queue.put(StopIteration)

class ChainStreamHandler(StreamingStdOutCallbackHandler):
    def __init__(self, gen):
        super().__init__()
        self.gen = gen

    def on_llm_new_token(self, token: str, **kwargs):
        self.gen.send(token)

def llm_thread(g, prompt):
    try:
        llm = OpenAI(
            verbose=True,
            streaming=True,
            callbacks=[ChainStreamHandler(g)],
            temperature=0.7,
        )
        llm(prompt)
    finally:
        g.close()


def chain(prompt):
    g = ThreadedGenerator()
    threading.Thread(target=llm_thread, args=(g, prompt)).start()
    return g


@app.route('/chain', methods=['POST'])
def _chain():
    return Response(chain("# A koan story about AGI\n\n"), mimetype='text/plain')

if __name__ == '__main__':
    app.run(threaded=True, debug=True, host='0.0.0.0', port=8080)