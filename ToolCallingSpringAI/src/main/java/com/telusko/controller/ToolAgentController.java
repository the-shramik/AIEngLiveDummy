package com.telusko.controller;

import com.telusko.tools.DateTimeTools;
import com.telusko.tools.ProductTools;
import com.telusko.tools.WishlistTools;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/tool")
public class ToolAgentController {

    private final ChatClient chatClient;
    private final ProductTools productTools;
    private final DateTimeTools dateTimeTools;
    private final WishlistTools wishlistTools;

    public ToolAgentController(ChatClient.Builder builder, ProductTools productTools,DateTimeTools dateTimeTools,WishlistTools wishlistTools) {
        this.productTools = productTools;
        this.chatClient = builder.build();
        this.dateTimeTools = dateTimeTools;
        this.wishlistTools = wishlistTools;
    }


    // Tool: getCurrentLocalTime()
    // Example: http://localhost:8080/api/tool/local-time?message=what is my current local time
    @GetMapping("/local-time")
    public String localTime(@RequestParam String message) {

        return chatClient.prompt()
                .user(message)
                .tools(dateTimeTools)
                .call()
                .content();
    }

    /// Tool: getCurrentTime(timeZone)
    // Example: http://localhost:8080/api/tool/time?message=what time is it in Europe/London
    @GetMapping("/time")
    public String time(@RequestParam String message) {

        return chatClient.prompt()
                .user(message)
                .tools(dateTimeTools)
                .call()
                .content();
    }

    @GetMapping("/products")
    public String ask(@RequestParam String query) {

        String system = """
                 You are a product assistant for a small catalog.
                    For any product question, call the tool `search_products` first.
                    Answer ONLY using the tool results. If not found, say "I don't know".
                """;

        return chatClient.prompt()
                .system(system)
                .user(query)
                .tools(productTools)
                .call()
                .content();
    }

    // Example: http://localhost:8080/api/tool/wishlist?message=Save Bluetooth Wireless Earbuds to wishlist&username=navin
    @GetMapping("/wishlist")
    public String wishlist(@RequestParam String message, @RequestParam String username) {

        String system = """
            You are an assistant that can save products.
            If the user asks to save/add/bookmark a product, call the tool `save_to_wishlist`.
            Always store the exact title mentioned by the user.
            """;

        return chatClient.prompt()
                .system(system)
                .user("username=" + username + "\n" + message)
                .tools(wishlistTools)
                .call()
                .content();
    }

    // Example: http://localhost:8080/api/tool/wishlist/view?message=show my wishlist&username=navin
    @GetMapping("/wishlist/view")
    public String viewWishlist(@RequestParam String message, @RequestParam String username) {
        return chatClient.prompt()
                .user("username=" + username + "\n" + message)
                .tools(wishlistTools)
                .call()
                .content();
    }
}
