crear entorno virtual
```
python -m venv .venv
```

activar entorno virtual
```
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### Adicional
1. En ARM instalar: https://rustup.rs
2. Reiniciar consola e instalar
```
pip install --upgrade pip setuptools wheel
pip install langchain-openai
```

#### Para visualizar graqfos
https://mermaidviewer.com/editor


### Arquitectura del proyecto
- main.py: Código del agente
- langgraph.json: Configuración de LangGraph
- requirements.txt: Dependencias del proyecto
- .env: Variables de entorno (API Keys)
- README.md: Documentación del proyecto

### Instalación de dependencias
```
pip install -r requirements.txt
```

### Configuración de variables de entorno
Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:
```
OPENAI_API_KEY=tu_openai_api_key_aqui
ANTHROPIC_API_KEY=tu_anthropic_api_key_aqui
DEEPSEEK_API_KEY=tu_deepseek_api_key_aqui
```


### Adicional en No ARM = Ejecución del agente con LangGraph CLI
```
langgraph --help
langgraph dev
```

Para esto se necesita tener instalado LangGraph CLI.
```
pip install -U "langgraph-cli[inmem]"
```
Pero no funciona para ARM.

### Con conda
```
conda create -n langgraph python=3.11 openssl cryptography grpcio -y
conda activate langgraph

conda install -c conda-forge openssl cryptography grpcio protobuf rust pip


pip install -r requirements.txt
```

#### UV en conda
```
pip install uv

# BASE 
uv --version 

# deactivate the virtual environment 
deactivate 
rm -rf .venv 

## init 
uv init 
uv venv # no en conda ------------------------

# add dependencies 
uv add langgraph langchain langchain-openai 
uv add "langgraph-cli[inmem]" --dev
uv add grandalf --dev
uv add jinja2 
uv add langchain[google-genai] langchain-deepseek langchain-google-vertexai langchain-anthropic
uv add "fastapi[standard]"

# add ipykernel for jupyter 
uv add ipykernel--dev
python -m ipykernel install --user --name agents --display-name "Agents (ARM)" # Conda ************
conda install -n langgraph ipykernel --update-deps --force-reinstall


# run the agent ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
uv run langgraph dev 



# AGREGA AL FINAL DEL PYPROJECT.TOML ++++++++++++++++++
[tool.setuptools.packages.find]
where = ["src"]
include = ["*"]

# Y luego como recompilar el proyecto ++++++++++++++++++
# install the project
uv pip install -e .

```

### FastAPI + Uvicorn
```
uv add "fastapi[standard]"

uv run fastapi dev ./src/api/main.py
```

```
normalmente es
fastapi dev ./src/api/main.py

uv add langgraph-checkpoint-postgres
```




