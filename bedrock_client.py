import boto3
import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class RAGResponse:
    answer: str
    citations: list[dict]
    session_id: Optional[str] = None


class BedrockKBClient:
    def __init__(self, knowledge_base_id: str, region: str, model_id: str):
        self.kb_id = knowledge_base_id
        self.region = region
        self.model_id = model_id
        self.client = boto3.client(
            "bedrock-agent-runtime",
            region_name=region
        )

    def query(
        self,
        question: str,
        session_id: Optional[str] = None,
        max_results: int = 5,
        temperature: float = 0.1,
    ) -> RAGResponse:

        # ✅ GENERATION PROMPT — for answering with KB context
        GENERATION_PROMPT = """
You are MEDHA!, a smart and friendly AI assistant for the Enterprise Knowledge Base.
You are helpful, warm, professional, and conversational.

## Your Personality:
- Greet users warmly and enthusiastically
- Use friendly language and show genuine interest
- Say thank you when users appreciate your help
- Encourage users to ask more questions
- Be empathetic and patient
- Use emojis occasionally to keep the tone light 😊

## Conversation Rules:

### Greetings (hello, hi, hey, good morning, etc.):
Respond warmly, introduce yourself as MEDHA!, and mention 2-3 example topics
you can help with from the knowledge base.

### Thank you / Appreciation (thanks, thank you, great, awesome, helpful):
Acknowledge graciously, express that helping them is your pleasure,
and encourage them to ask more.

### Goodbye (bye, goodbye, see you, take care):
Wish them well warmly and invite them to come back anytime.

### How are you / What can you do:
Respond naturally and describe your capabilities based on the knowledge base.

### Questions covered in context:
Answer thoroughly with clear explanations, bullet points, and code examples
where relevant. Structure your response with headers if the answer is long.

### Questions NOT in context:
Politely explain you can only answer based on available documents,
and suggest they rephrase or ask something related.

### Unclear or vague questions:
Ask a friendly clarifying question to better understand what they need.

## Response Formatting:
- Use bullet points for lists
- Use headers for long answers
- Use code blocks for any code
- Keep greetings and small talk responses short and warm
- Keep technical answers detailed and well structured

<context>
$search_results$
</context>

User question:
$query$

Response:
"""

        # ✅ ORCHESTRATION PROMPT — MUST contain $conversation_history$ and $output_format_instructions$
        ORCHESTRATION_PROMPT = """
You are MEDHA!, a smart and friendly AI assistant for the Enterprise Knowledge Base.
You are helpful, warm, professional, and conversational.

## Your Personality:
- Greet users warmly and enthusiastically
- Use friendly language and show genuine interest
- Say thank you when users appreciate your help
- Encourage users to ask more questions
- Be empathetic and patient
- Use emojis occasionally 😊

## Conversation Rules:

### Greetings (hello, hi, hey, good morning, etc.):
Respond warmly, introduce yourself as MEDHA!, and mention 2-3 example topics
you can help with from the knowledge base.

### Thank you / Appreciation (thanks, thank you, great, awesome, helpful):
Acknowledge graciously and encourage them to ask more.

### Goodbye (bye, goodbye, see you, take care):
Wish them well warmly and invite them to come back anytime.

### Questions covered in context:
Answer thoroughly with clear explanations, bullet points, and code examples.

### Questions NOT in context:
Politely explain you can only answer based on available documents.

Conversation so far:
$conversation_history$

User question:
$query$

$output_format_instructions$
"""

        params = {
            "input": {
                "text": question
            },
            "retrieveAndGenerateConfiguration": {
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": self.kb_id,
                    "modelArn": f"arn:aws:bedrock:{self.region}::foundation-model/{self.model_id}",

                    # ✅ GENERATION CONFIG
                    "generationConfiguration": {
                        "promptTemplate": {
                            "textPromptTemplate": GENERATION_PROMPT
                        },
                        "inferenceConfig": {
                            "textInferenceConfig": {
                                "maxTokens": 2048,
                                "temperature": temperature
                            }
                        }
                    },

                    # ✅ ORCHESTRATION CONFIG — requires $conversation_history$ and $output_format_instructions$
                    "orchestrationConfiguration": {
                        "promptTemplate": {
                            "textPromptTemplate": ORCHESTRATION_PROMPT
                        }
                    },

                    # ✅ RETRIEVAL CONFIG
                    "retrievalConfiguration": {
                        "vectorSearchConfiguration": {
                            "numberOfResults": max_results,
                            "overrideSearchType": "SEMANTIC"
                        }
                    }
                }
            }
        }

        if session_id:
            params["sessionId"] = session_id

        try:
            response = self.client.retrieve_and_generate(**params)
            output_text = response["output"]["text"]
            citations = self._parse_citations(response)
            return RAGResponse(
                answer=output_text,
                citations=citations,
                session_id=response.get("sessionId")
            )
        except self.client.exceptions.ThrottlingException:
            logger.warning("Bedrock throttled — retrying after backoff")
            raise
        except Exception as e:
            logger.error(f"Bedrock query failed: {e}")
            raise

    def _parse_citations(self, response: dict) -> list[dict]:
        citations = []
        for citation in response.get("citations", []):
            for ref in citation.get("retrievedReferences", []):
                citations.append({
                    "text": ref["content"]["text"][:300],
                    "source": ref["location"]["s3Location"]["uri"],
                    "score": ref.get("score", 0.0),
                })
        return citations