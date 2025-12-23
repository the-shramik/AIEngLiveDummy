package com.telusko.tools;

import org.springframework.ai.document.Document;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.lang.Nullable;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class ProductTools {

    private final VectorStore vectorStore;

    public ProductTools(VectorStore vectorStore) {
        this.vectorStore = vectorStore;
    }

    @Tool(
            name = "search_products",
            description = """
            Search the product catalog using semantic similarity.
            Use this whenever the user asks about products, price, category, features, or comparisons.
            """
    )
    public List<String> searchProducts(
            @ToolParam(description = "User query, e.g. 'wireless earbuds under $50'") String query,
            @ToolParam(description = "How many results to return (1-5).", required = false)
            @Nullable Integer topK
    ) {
        int k = (topK == null) ? 3 : Math.max(1, Math.min(topK, 5));

        List<Document> docs = vectorStore.similaritySearch(
                SearchRequest.builder().query(query).topK(k).build()
        );

        return docs.stream().map(Document::getFormattedContent).toList();
    }
}
