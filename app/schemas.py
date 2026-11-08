from pydantic import BaseModel, Field


class RewriteRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=5000,
        description="The original message to rewrite."
    )
    tone: str = Field(default="professional")
    length: str = Field(default="balanced")
    recipient: str = Field(default="colleague")


class RewriteResponse(BaseModel):
    rewritten_message: str
