from typing import List, Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from whatsapp import (
    search_contacts as whatsapp_search_contacts,
    list_messages as whatsapp_list_messages,
    list_chats as whatsapp_list_chats,
    get_chat as whatsapp_get_chat,
    get_direct_chat_by_contact as whatsapp_get_direct_chat_by_contact,
    get_contact_chats as whatsapp_get_contact_chats,
    get_last_interaction as whatsapp_get_last_interaction,
    get_message_context as whatsapp_get_message_context,
    send_message as whatsapp_send_message,
    send_file as whatsapp_send_file,
    send_audio_message as whatsapp_audio_voice_message,
    download_media as whatsapp_download_media
)

# Initialize FastMCP server
mcp = FastMCP("whatsapp")

@mcp.tool()
def search_contacts(query: str) -> List[Dict[str, Any]]:
    """Buscar contatos do WhatsApp por nome ou número de telefone.
    
    Args:
        query: Termo de busca para corresponder a nomes de contatos ou números de telefone
    """
    contacts = whatsapp_search_contacts(query)
    return contacts

@mcp.tool()
def list_messages(
    after: Optional[str] = None,
    before: Optional[str] = None,
    sender_phone_number: Optional[str] = None,
    chat_jid: Optional[str] = None,
    query: Optional[str] = None,
    limit: int = 20,
    page: int = 0,
    include_context: bool = True,
    context_before: int = 1,
    context_after: int = 1
) -> List[Dict[str, Any]]:
    """Obter mensagens do WhatsApp que correspondem aos critérios especificados com contexto opcional.
    
    Args:
        after: String opcional em formato ISO-8601 para retornar apenas mensagens após esta data
        before: String opcional em formato ISO-8601 para retornar apenas mensagens antes desta data
        sender_phone_number: Número de telefone opcional para filtrar mensagens por remetente
        chat_jid: JID de conversa opcional para filtrar mensagens por conversa
        query: Termo de busca opcional para filtrar mensagens por conteúdo
        limit: Número máximo de mensagens a retornar (padrão 20)
        page: Número da página para paginação (padrão 0)
        include_context: Se deve incluir mensagens antes e depois das correspondências (padrão True)
        context_before: Número de mensagens a incluir antes de cada correspondência (padrão 1)
        context_after: Número de mensagens a incluir depois de cada correspondência (padrão 1)
    """
    messages = whatsapp_list_messages(
        after=after,
        before=before,
        sender_phone_number=sender_phone_number,
        chat_jid=chat_jid,
        query=query,
        limit=limit,
        page=page,
        include_context=include_context,
        context_before=context_before,
        context_after=context_after
    )
    return messages

@mcp.tool()
def list_chats(
    query: Optional[str] = None,
    limit: int = 20,
    page: int = 0,
    include_last_message: bool = True,
    sort_by: str = "last_active"
) -> List[Dict[str, Any]]:
    """Obter conversas do WhatsApp que correspondem aos critérios especificados.
    
    Args:
        query: Termo de busca opcional para filtrar conversas por nome ou JID
        limit: Número máximo de conversas a retornar (padrão 20)
        page: Número da página para paginação (padrão 0)
        include_last_message: Se deve incluir a última mensagem em cada conversa (padrão True)
        sort_by: Campo para ordenar os resultados, "last_active" ou "name" (padrão "last_active")
    """
    chats = whatsapp_list_chats(
        query=query,
        limit=limit,
        page=page,
        include_last_message=include_last_message,
        sort_by=sort_by
    )
    return chats

@mcp.tool()
def get_chat(chat_jid: str, include_last_message: bool = True) -> Dict[str, Any]:
    """Obter metadados da conversa do WhatsApp por JID.
    
    Args:
        chat_jid: O JID da conversa a ser recuperada
        include_last_message: Se deve incluir a última mensagem (padrão True)
    """
    chat = whatsapp_get_chat(chat_jid, include_last_message)
    return chat

@mcp.tool()
def get_direct_chat_by_contact(sender_phone_number: str) -> Dict[str, Any]:
    """Obter metadados da conversa do WhatsApp por número de telefone do remetente.
    
    Args:
        sender_phone_number: O número de telefone a ser pesquisado
    """
    chat = whatsapp_get_direct_chat_by_contact(sender_phone_number)
    return chat

@mcp.tool()
def get_contact_chats(jid: str, limit: int = 20, page: int = 0) -> List[Dict[str, Any]]:
    """Obter todas as conversas do WhatsApp envolvendo o contato.
    
    Args:
        jid: O JID do contato a ser pesquisado
        limit: Número máximo de conversas a retornar (padrão 20)
        page: Número da página para paginação (padrão 0)
    """
    chats = whatsapp_get_contact_chats(jid, limit, page)
    return chats

@mcp.tool()
def get_last_interaction(jid: str) -> str:
    """Obter a mensagem mais recente do WhatsApp envolvendo o contato.
    
    Args:
        jid: O JID do contato a ser pesquisado
    """
    message = whatsapp_get_last_interaction(jid)
    return message

@mcp.tool()
def get_message_context(
    message_id: str,
    before: int = 5,
    after: int = 5
) -> Dict[str, Any]:
    """Obter contexto ao redor de uma mensagem específica do WhatsApp.
    
    Args:
        message_id: O ID da mensagem para obter o contexto
        before: Número de mensagens a incluir antes da mensagem alvo (padrão 5)
        after: Número de mensagens a incluir depois da mensagem alvo (padrão 5)
    """
    context = whatsapp_get_message_context(message_id, before, after)
    return context

@mcp.tool()
def send_message(
    recipient: str,
    message: str
) -> Dict[str, Any]:
    """Enviar uma mensagem do WhatsApp para uma pessoa ou grupo. Para conversas em grupo, use o JID.

    Args:
        recipient: O destinatário - pode ser um número de telefone com código do país mas sem + ou outros símbolos,
                 ou um JID (por exemplo, "123456789@s.whatsapp.net" ou um JID de grupo como "123456789@g.us")
        message: O texto da mensagem a enviar
    
    Returns:
        Um dicionário contendo o status de sucesso e uma mensagem de status
    """
    # Validar entrada
    if not recipient:
        return {
            "success": False,
            "message": "O destinatário deve ser fornecido"
        }
    
    # Chamar a função whatsapp_send_message com o parâmetro unificado recipient
    success, status_message = whatsapp_send_message(recipient, message)
    return {
        "success": success,
        "message": status_message
    }

@mcp.tool()
def send_file(recipient: str, media_path: str) -> Dict[str, Any]:
    """Enviar um arquivo como imagem, áudio bruto, vídeo ou documento via WhatsApp para o destinatário especificado. Para mensagens em grupo, use o JID.
    
    Args:
        recipient: O destinatário - pode ser um número de telefone com código do país mas sem + ou outros símbolos,
                 ou um JID (por exemplo, "123456789@s.whatsapp.net" ou um JID de grupo como "123456789@g.us")
        media_path: O caminho absoluto para o arquivo de mídia a enviar (imagem, vídeo, documento)
    
    Returns:
        Um dicionário contendo o status de sucesso e uma mensagem de status
    """
    
    # Chamar a função whatsapp_send_file
    success, status_message = whatsapp_send_file(recipient, media_path)
    return {
        "success": success,
        "message": status_message
    }

@mcp.tool()
def send_audio_message(recipient: str, media_path: str) -> Dict[str, Any]:
    """Enviar qualquer arquivo de áudio como uma mensagem de áudio do WhatsApp para o destinatário especificado. Para mensagens em grupo, use o JID. Se houver erro devido ao ffmpeg não estar instalado, use send_file em vez disso.
    
    Args:
        recipient: O destinatário - pode ser um número de telefone com código do país mas sem + ou outros símbolos,
                 ou um JID (por exemplo, "123456789@s.whatsapp.net" ou um JID de grupo como "123456789@g.us")
        media_path: O caminho absoluto para o arquivo de áudio a enviar (será convertido para Opus .ogg se não for um arquivo .ogg)
    
    Returns:
        Um dicionário contendo o status de sucesso e uma mensagem de status
    """
    success, status_message = whatsapp_audio_voice_message(recipient, media_path)
    return {
        "success": success,
        "message": status_message
    }

@mcp.tool()
def download_media(message_id: str, chat_jid: str) -> Dict[str, Any]:
    """Baixar mídia de uma mensagem do WhatsApp e obter o caminho do arquivo local.
    
    Args:
        message_id: O ID da mensagem contendo a mídia
        chat_jid: O JID da conversa contendo a mensagem
    
    Returns:
        Um dicionário contendo o status de sucesso, uma mensagem de status e o caminho do arquivo se bem-sucedido
    """
    file_path = whatsapp_download_media(message_id, chat_jid)
    
    if file_path:
        return {
            "success": True,
            "message": "Mídia baixada com sucesso",
            "file_path": file_path
        }
    else:
        return {
            "success": False,
            "message": "Falha ao baixar a mídia"
        }

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')