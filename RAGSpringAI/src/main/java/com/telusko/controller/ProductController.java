package com.telusko.controller;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.document.Document;
import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.stream.Collectors;

@RestController
public class ProductController {

    private final VectorStore vectorStore;
    private final ChatClient chatClient;

    public ProductController(VectorStore vectorStore, ChatClient chatClient) {
        this.vectorStore = vectorStore;
        this.chatClient = chatClient;
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

    @GetMapping("/product/ask")
    public String askProductQuestion(@RequestParam String question) {

        // R – Retrieval
        SearchRequest request = SearchRequest.builder()
                .query(question)
                .topK(5)
                .build();

        List<Document> docs = vectorStore.similaritySearch(request);

        // A – Augmented context
        StringBuilder context = new StringBuilder();
        for (Document document : docs) {
            context.append(document.getFormattedContent()).append("\n");
        }

        // G – Generation
        String prompt = """
                You are a helpful product suggestion assistant.
                Use only the information in the product details below to answer the user.
                If the information is not available there, say you don't know.

                Product details:
                %s

                User question: %s

                Answer in a short, clear way:
                """.formatted(context, question);

        return chatClient
                .prompt()
                .user(prompt)
                .call()
                .content();
    }
}
