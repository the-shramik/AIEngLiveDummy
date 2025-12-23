package com.telusko.controller;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.image.ImageModel;
import org.springframework.ai.image.ImagePrompt;
import org.springframework.ai.image.ImageResponse;
import org.springframework.ai.openai.OpenAiImageOptions;
import org.springframework.util.MimeTypeUtils;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class ImageController {

    private final ChatClient chatClient;

    private final ImageModel imageModel;

    public ImageController(ChatClient.Builder chatClient, ImageModel imageModel) {
        this.chatClient = chatClient.build();
        this.imageModel = imageModel;

    }

    @GetMapping("/image/{query}")
    public String generateImage(@PathVariable String query) {
        ImagePrompt prompt = new ImagePrompt(query, OpenAiImageOptions.builder()
                .N(1)
                .width(1024)
                .height(1024)
                .quality("hd")
                .responseFormat("url")
                .model("dall-e-3")
                .build());

        ImageResponse response = imageModel.call(prompt);
        return response.getResult().getOutput().getUrl();
    }

    @PostMapping("/image/describe")
    public String describeImage(@RequestParam String query, @RequestParam MultipartFile file) {
        return chatClient.prompt()
                .user(us -> us.text(query)
                        .media(MimeTypeUtils.IMAGE_JPEG, file.getResource()))
                .call()
                .content();
    }

}
