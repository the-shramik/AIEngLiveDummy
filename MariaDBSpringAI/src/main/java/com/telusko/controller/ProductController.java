package com.telusko.controller;

import org.springframework.ai.document.Document;
import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
public class ProductController {

    private final VectorStore vectorStore;

    public ProductController(VectorStore vectorStore) {
        this.vectorStore = vectorStore;
    }

    @PostMapping("/api/product")
    public List<Document> getProducts(@RequestParam String text) {

        SearchRequest request = SearchRequest.builder()
                .query(text)
                .topK(5)
                .similarityThreshold(0.78)
                .build();

        return vectorStore.similaritySearch(request);
    }
}
