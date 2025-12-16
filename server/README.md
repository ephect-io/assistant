# Inference server setup For AMD FX9370

## Fine tuning

```bash
dnf install -y kernel-tools
cpupower frequency-set -g performance
cpupower frequency-set -u 3.4GHz
```

## LLaMA.cpp Server Setup

### Package Installation

```bash
dnf install -y gcc-c++ make cmake libcurl-devel ccache
```

```bash
mkdir -p /opt/llm/
cd /opt/llm/
```
```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
cmake  -B build -DLLAMA_CUDA=OFF -DLLAMA_METAL=OFF -DLLAMA_OPENCL=OFF
cmake --build build --config Server -j 8
```

### Model Preparation

Download a compatible LLaMA model in GGML format and place it in the `models` directory. For example:

### Python Client Setup

```bash
pip install huggingface_hub
pip install requests
```

Login to Hugging Face if needed:
 
```bash
hf login --token $(cat ../../../assets/assistant/hugging-face/token.txt)
```

Download the model:

⚠️  Warning: 'huggingface-cli download' is deprecated. Use 'hf download' instead.

```bash
hf download Qwen/Qwen2.5-Coder-1.5B --local-dir /opt/llm/hugging-face/models --local-dir-use-symlinks False
```

Convert the model to GGUF format:

```bash
python3 convert_hf_to_gguf.py   --outtype auto   --outfile ./models/qwen2_5-coder-1_5b-q4_0.gguf   ../hugging-face/models/Qwen2.5-Coder-1.5B
```

### Running the Server

```bash
./build/bin/llama-server -m ./models/qwen2_5-coder-1_5b-q4_0.gguf
``` 

#### Test Request

```bash
curl -X POST http://localhost:8080/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ggml-model-q4_0.bin",
    "prompt": "Hello, how are you?",
    "max_tokens": 50,
    "temperature": 0.7
  }'
```
#### Expected Response

```bash
{
  "id": "cmpl-xxxxxxxxxxxx",
  "object": "text_completion",
  "created": 1633036800,
  "model": "ggml-model-q4_0.bin",
  "choices": [
    {
      "text": " I'm doing well, thank you! How can I assist you today?",
      "index": 0,
      "logprobs": null,
      "finish_reason": "length"
    }
  ],
  "usage": {
    "prompt_tokens": 5,
    "completion_tokens": 15,
    "total_tokens": 20
  }
}
```

## Systemd service setup

`/etc/systemd/system/llama-server.service`:

```conf
[Unit]
Description=Local LLM Inference Server
After=network.target

[Service]
Type=simple
User=llm
Group=llm
ExecStart=/opt/llm/llama-server \
  -m /opt/llm/models/qwen2.5-coder-1.5b-q4.gguf \
  -t 6 \
  -c 4096 \
  --host 127.0.0.1 \
  --port 8081
Restart=always
RestartSec=5

# Sécurité / stabilité FX-9370
CPUQuota=70%
MemoryMax=6G
Nice=10
IOSchedulingClass=best-effort
IOSchedulingPriority=6

NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true

[Install]
WantedBy=multi-user.target
```

### Activate service

```bash
systemctl daemon-reexec
systemctl daemon-reload
systemctl enable --now llama-server
systemctl status llama-server
```

### Test server

```bash
curl http://127.0.0.1:8081/health
```

## NOTES
- Make sure to replace `./models/ggml-model-q4_0.bin` with  the path to your actual model file. 
- You can adjust the server parameters and request payload as needed for your specific use case.
- This setup assumes you have a compatible model file in the specified format.
- For production use, consider additional configurations for security, scalability, and performance.
- Refer to the llama.cpp documentation for more advanced options and configurations.
- This server implementation is basic and may not include all features of more robust serving solutions.
- Ensure your environment meets all dependencies required by llama.cpp.
- Test with different prompts and parameters to evaluate model performance.
- Monitor server logs for any issues during operation.
- Consider using a process manager for production deployments to ensure the server remains running.
- Regularly update the llama.cpp repository to benefit from improvements and bug fixes.
- Explore additional features of the llama.cpp server, such as streaming responses or custom endpoints, as needed.
- This README provides a foundational guide to setting up and running a basic server for serving LLaMA models using the llama.cpp implementation.
- For further customization and advanced usage, refer to the official llama.cpp GitHub repository and documentation.
- Happy coding and model serving!

