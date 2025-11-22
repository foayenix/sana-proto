"""
SANA Messaging Routes
Client-practitioner communication
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

router = APIRouter()


# ============================================================================
# SCHEMAS
# ============================================================================

class Conversation(BaseModel):
    id: str
    participant_1_id: str
    participant_1_name: str
    participant_2_id: str
    participant_2_name: str
    last_message: Optional[str] = None
    last_message_at: Optional[datetime] = None
    unread_count: int = 0


class Message(BaseModel):
    id: str
    conversation_id: str
    sender_id: str
    sender_name: str
    content: str
    is_read: bool = False
    created_at: datetime


class MessageSend(BaseModel):
    content: str
    sender_id: str


# ============================================================================
# MOCK DATA
# ============================================================================

CONVERSATIONS = [
    {
        "id": "conv_001",
        "participant_1_id": "client_001",
        "participant_1_name": "Sarah Mitchell",
        "participant_2_id": "prac_001",
        "participant_2_name": "Dr. Emily Chen",
        "last_message": "See you at our next session!",
        "last_message_at": datetime(2024, 6, 20, 14, 30),
        "unread_count": 0
    },
    {
        "id": "conv_002",
        "participant_1_id": "client_001",
        "participant_1_name": "Sarah Mitchell",
        "participant_2_id": "prac_002",
        "participant_2_name": "Sarah Johnson",
        "last_message": "I've attached the diet recommendations",
        "last_message_at": datetime(2024, 6, 18, 10, 15),
        "unread_count": 1
    }
]

MESSAGES = [
    {
        "id": "msg_001",
        "conversation_id": "conv_001",
        "sender_id": "client_001",
        "sender_name": "Sarah Mitchell",
        "content": "Hi Dr. Chen, I wanted to let you know the anxiety has been much better this week!",
        "is_read": True,
        "created_at": datetime(2024, 6, 20, 10, 0)
    },
    {
        "id": "msg_002",
        "conversation_id": "conv_001",
        "sender_id": "prac_001",
        "sender_name": "Dr. Emily Chen",
        "content": "That's wonderful to hear! Keep up with the breathing exercises. See you at our next session!",
        "is_read": True,
        "created_at": datetime(2024, 6, 20, 14, 30)
    }
]


# ============================================================================
# ROUTES
# ============================================================================

@router.post("/conversations", response_model=Conversation)
async def start_conversation(participant_1_id: str, participant_2_id: str):
    """
    Start a new conversation

    Creates messaging thread between:
    - Client and practitioner
    - Or any two users
    """
    # Check if conversation exists
    existing = next(
        (c for c in CONVERSATIONS
         if (c["participant_1_id"] == participant_1_id and c["participant_2_id"] == participant_2_id) or
            (c["participant_1_id"] == participant_2_id and c["participant_2_id"] == participant_1_id)),
        None
    )

    if existing:
        return Conversation(**existing)

    conv_id = f"conv_{uuid.uuid4().hex[:8]}"

    return Conversation(
        id=conv_id,
        participant_1_id=participant_1_id,
        participant_1_name="User",  # Would lookup from DB
        participant_2_id=participant_2_id,
        participant_2_name="Practitioner",
        unread_count=0
    )


@router.get("/conversations/{user_id}")
async def list_conversations(user_id: str, limit: int = Query(default=20, le=50)):
    """
    List user's conversations

    Returns:
    - All conversations
    - Last message preview
    - Unread count
    """
    user_conversations = [
        c for c in CONVERSATIONS
        if c["participant_1_id"] == user_id or c["participant_2_id"] == user_id
    ]

    return {
        "user_id": user_id,
        "conversations": [Conversation(**c) for c in user_conversations],
        "total": len(user_conversations)
    }


@router.post("/conversations/{conversation_id}/messages", response_model=Message)
async def send_message(conversation_id: str, data: MessageSend):
    """
    Send a message in a conversation

    Features:
    - Text messages
    - Read receipts
    - Push notifications (async)
    """
    msg_id = f"msg_{uuid.uuid4().hex[:8]}"

    new_message = Message(
        id=msg_id,
        conversation_id=conversation_id,
        sender_id=data.sender_id,
        sender_name="User",  # Would lookup
        content=data.content,
        is_read=False,
        created_at=datetime.utcnow()
    )

    return new_message


@router.get("/conversations/{conversation_id}/messages")
async def get_messages(
    conversation_id: str,
    before: Optional[datetime] = None,
    limit: int = Query(default=50, le=100)
):
    """
    Get messages in a conversation

    Pagination:
    - Load recent messages
    - Use 'before' for older messages
    """
    conv_messages = [m for m in MESSAGES if m["conversation_id"] == conversation_id]

    if before:
        conv_messages = [m for m in conv_messages if m["created_at"] < before]

    # Sort by date descending
    conv_messages.sort(key=lambda x: x["created_at"], reverse=True)

    return {
        "conversation_id": conversation_id,
        "messages": [Message(**m) for m in conv_messages[:limit]],
        "has_more": len(conv_messages) > limit
    }


@router.post("/conversations/{conversation_id}/read")
async def mark_as_read(conversation_id: str, user_id: str):
    """
    Mark all messages as read

    Updates:
    - Message read status
    - Conversation unread count
    """
    return {
        "conversation_id": conversation_id,
        "marked_read": True,
        "updated_count": 2
    }


@router.get("/unread-count/{user_id}")
async def get_unread_count(user_id: str):
    """
    Get total unread message count

    Used for:
    - Badge notifications
    - Inbox indicator
    """
    user_conversations = [
        c for c in CONVERSATIONS
        if c["participant_1_id"] == user_id or c["participant_2_id"] == user_id
    ]

    total_unread = sum(c["unread_count"] for c in user_conversations)

    return {
        "user_id": user_id,
        "unread_count": total_unread,
        "conversations_with_unread": sum(1 for c in user_conversations if c["unread_count"] > 0)
    }
