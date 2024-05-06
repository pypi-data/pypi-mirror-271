from langchain_core.documents import Document as LangchainDocument

from bot_station.domain.bot.model.document import Document

SOURCE_LINK_KEY = "source_link"
ID_KEY = "id"


class DocumentMapper:

    @staticmethod
    def to_langchain_document(doc: Document) -> LangchainDocument:
        filled_metadata = doc.metadata
        if doc.source_link is not None:
            filled_metadata[SOURCE_LINK_KEY] = doc.source_link
        if doc.id is not None:
            filled_metadata[ID_KEY] = doc.id
        return LangchainDocument(page_content=doc.data, metadata=filled_metadata)

    @staticmethod
    def from_langchain_document(doc: LangchainDocument) -> Document:
        return Document(
            data=doc.page_content,
            metadata=doc.metadata,
            source_link=doc.metadata.get(SOURCE_LINK_KEY, None),
            id=doc.metadata.get(ID_KEY, ""),
        )
