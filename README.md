## Documentação da API - Geração de Flashcards com IA

## Visão Geral

Esta API permite gerar flashcards automaticamente a partir de um tema fornecido. Ela utiliza Inteligência Artificial para criar perguntas e respostas baseadas no contexto informado pelo usuário.
### URL Base 
```prompt
https://api-dackify-ia-1.onrender.com
```

### Endpoints
### 1. Gerar Flashcards

**Endpoint:**
```prompt
POST /api/generate_quests
```
**Descrição**: Recebe um tema e a quantidade de perguntas desejadas e retorna uma lista de flashcards (pergunta e resposta).

**Parâmetros da Requisição (JSON):**
```json
{
	"context": "História do Brasil",
	"quantidade_tasks": 5
}
```
**Resposta de Sucesso (200 OK):**
```json
{
  "message": "Ok",
  "flashcards": [
    {
      "frente": "Quem foi o primeiro imperador do Brasil?",
      "verso": "Dom Pedro I."
    },
    {
      "frente": "Qual foi o ano da Proclamação da Independência do Brasil?",
      "verso": "1822."
    }
  ]
}
```
**Possíveis Erros:**
- **400 Bad Request**: Se os campos obrigatórios "context" ou "quantidade tasks" não forem informados.
- **500 Internal Server Error:** Se houver falha na comunicação com a IA ou erro no processamento dos flashcards.

## Autenticação
Atualmente, a API não requer autenticação para uso.
