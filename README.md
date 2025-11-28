# 🐍 Python Template - AYU CODE STYLE

Template Python pronto para clonar e começar a codar. Segue o **AYU CODE STYLE**.

## 🚀 Quick Start

```bash
# clonar
git clone <repo> meu-projeto
cd meu-projeto

# criar venv
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# instalar
pip install -r requirements.txt

# rodar
python main.py
```

API disponível em `http://localhost:8000/docs`

## 📁 Estrutura

```
src/
├── core/                    # Tipos funcionais (Either, Option, Spec, etc)
├── domain/
│   ├── entities/            # Entidades
│   └── enums/               # Enums do domínio
├── application/
│   ├── handlers/            # Casos de uso
│   ├── services/            # Lógica de negócio
│   ├── specifications/      # Regras de validação
│   └── view_models/         # DTOs (Request/Response)
├── infrastructure/
│   ├── repositories/        # Acesso a dados
│   ├── services/            # Serviços externos
│   ├── config.py            # Configurações
│   └── dependencies.py      # Injeção de dependências
└── api/
    └── controllers/         # Endpoints HTTP

tests/
├── unit/                    # Testes unitários
└── integration/             # Testes de integração
```

## 🏗️ Fluxo

```
REQUEST → CONTROLLER → HANDLER → SERVICE → REPOSITORY
              ↓            ↓         ↓          ↓
          ViewModel    Command    Either    Entity
              ↓
          ApiResponse
              ↓
          RESPONSE
```

## 📦 Formato de Resposta Padrão

Todas as APIs retornam o mesmo formato:

```json
{
  "error": false,
  "error_message": null,
  "result": { ... }
}
```

### Sucesso

```json
{
  "error": false,
  "error_message": null,
  "result": {
    "id": "uuid",
    "name": "Produto"
  }
}
```

### Erro

```json
{
  "error": true,
  "error_message": "Nome ja existe",
  "result": null
}
```

### Paginado

```json
{
  "error": false,
  "error_message": null,
  "result": {
    "items": [...],
    "total": 100,
    "page": 1,
    "page_size": 10,
    "total_pages": 10
  }
}
```

## 🧪 Testes

```bash
pytest                    # todos
pytest tests/unit         # unitarios
pytest tests/integration  # integracao
pytest --cov=src          # com coverage
```

## 📝 Como Usar

### 1. Criar Entidade

```python
# src/domain/entities/produto.py
@dataclass
class Produto(AuditableEntity[UUID]):
    id: UUID = field(default_factory=generate_uuid)
    nome: str = ""
    preco: float = 0.0
    status: Status = Status.PENDING
```

### 2. Criar Enum (se necessário)

```python
# src/domain/enums/categoria.py
class Categoria(str, Enum):
    ELETRONICO = "eletronico"
    VESTUARIO = "vestuario"
```

### 3. Criar ViewModels

```python
# src/application/view_models/produto_vm.py
class CreateProdutoRequest(BaseModel):
    nome: str = Field(..., min_length=1)
    preco: float = Field(..., gt=0)

class ProdutoResponse(BaseModel):
    id: UUID
    nome: str
    preco: float
```

### 4. Criar Specifications

```python
# src/application/specifications/produto_specs.py
class PrecoPositivoSpec(Specification[float]):
    def is_satisfied_by(self, entity: float) -> bool:
        return entity > 0

    @property
    def error_message(self) -> str:
        return "Preco deve ser positivo"
```

### 5. Criar Service

```python
# src/application/services/produto_service.py
class ProdutoService:
    def __init__(self, repo: ProdutoRepository):
        self._repo = repo

    async def create(self, nome: str, preco: float) -> Either[ErrorResult, Produto]:
        # validacoes
        if not PrecoPositivoSpec().is_satisfied_by(preco):
            return Left(ErrorResult.validation("Preco invalido"))

        produto = Produto.create(nome=nome, preco=preco)
        return await self._repo.save(produto)
```

### 6. Criar Handler

```python
# src/application/handlers/produto_handler.py
class ProdutoHandler:
    def __init__(self, service: ProdutoService):
        self._service = service

    async def create(self, cmd: CreateProdutoCommand) -> Either[..., ProdutoResponse]:
        result = await self._service.create(cmd.nome, cmd.preco)
        return Right(to_response(result.value)) if result.is_right else result
```

### 7. Criar Controller

```python
# src/api/controllers/produto_controller.py
router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.post("", response_model=ProdutoResponse, status_code=201)
async def create(request: CreateProdutoRequest, handler: ProdutoHandlerDep):
    result = await handler.create(CreateProdutoCommand(nome=request.nome, preco=request.preco))
    return unwrap_or_raise(result)
```

### 8. Registrar Dependencies

```python
# src/infrastructure/dependencies.py
@lru_cache
def get_produto_repository() -> InMemoryProdutoRepository:
    return InMemoryProdutoRepository()

def get_produto_service(repo = Depends(get_produto_repository)) -> ProdutoService:
    return ProdutoService(repo)

ProdutoHandlerDep = Annotated[ProdutoHandler, Depends(get_produto_handler)]
```

### 9. Registrar Controller

```python
# src/api/controllers/__init__.py
from src.api.controllers.produto_controller import router as produto_router

# src/api/app.py
app.include_router(produto_router)
```

## ⚡ Padrões Funcionais

### Either

```python
from src.core import Either, Left, Right, match

result: Either[ErrorResult, Produto] = await service.create(...)

# match
output = match(result,
    on_left=lambda e: f"Erro: {e}",
    on_right=lambda v: f"Sucesso: {v}"
)
```

### Specification

```python
from src.core import Specification

spec = PrecoPositivoSpec() & NomeNotEmptySpec()
result = spec.validate(produto)  # Either[ErrorResult, Produto]
```

### Logger

```python
from src.core import logger, info, error, get_logger

# usar direto
info("Processando...")
error("Falhou!")

# ou pegar logger especifico
log = get_logger("meu_modulo")
log.info("Mensagem")
```

## 🚀 CI/CD

O projeto inclui workflows prontos:

- **CI** (`.github/workflows/ci.yml`):
  - Lint com Ruff
  - Testes com Pytest + Coverage
  - Build do pacote

- **CD** (`.github/workflows/cd.yml`):
  - Build Docker image
  - Push para GitHub Container Registry
  - Deploy staging/production

### Docker

```bash
# build
docker build -t app .

# run
docker run -p 8000:8000 app
```

---

**Clone e comece a codar!**
