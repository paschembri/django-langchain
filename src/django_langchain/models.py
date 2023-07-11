import os
from django.db import models
from pgvector.django import VectorField, CosineDistance
from langchain.document_loaders import UnstructuredFileLoader
from langchain.docstore.base import Docstore
from langchain.embeddings.huggingface import HuggingFaceEmbeddings


embedding_model = HuggingFaceEmbeddings()


class SourceDocument(models.Model):
    title = models.CharField(blank=True, default="")
    file = models.FileField()
    indexed = models.BooleanField(default=False)

    def parse_file(self, compute_embeddings=True):
        loader = UnstructuredFileLoader(self.file.path, mode="elements")

        docs = []
        for index, doc in enumerate(loader.load(), start=1):
            docs.append(
                DocumentChunk(
                    index=index,
                    metadata=doc.metadata,
                    page_content=doc.page_content,
                    source=self,
                )
            )

        if compute_embeddings:
            for doc in docs:
                doc.embedding = embedding_model.embed_query(doc.page_content)

        DocumentChunk.objects.bulk_create(docs)
        self.indexed = True
        self.save()


class DocumentChunkManager(models.Manager):
    def search(self, query, max_results=5):
        query_embedding = embedding_model.embed_query(query)

        results = DocumentChunk.objects.order_by(
            CosineDistance("embedding", query_embedding)
        )[:max_results]

        return results


class DocumentChunk(models.Model):
    index = models.IntegerField()
    metadata = models.JSONField()
    page_content = models.TextField()
    embedding = VectorField(dimensions=768)
    source = models.ForeignKey(SourceDocument, on_delete=models.CASCADE)

    objects = DocumentChunkManager()

    def __str__(self):
        source = os.path.basename(self.metadata.get("source"))

        return f"[{source}][chunk:{self.index}] p{self.metadata.get('page_number')}"


class DocumentChunkStore(Docstore):
    def search(self, search: str):
        """
        Perform a similarity search throughout documents (i.e. text chunks)
        """
        chunk = DocumentChunk.objects.search(search)[0]
        return chunk.metadata.get("source"), chunk
