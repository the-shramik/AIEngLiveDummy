package com.telusko.tools;

import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Component
public class WishlistTools {

    private final Map<String, List<String>> wishlistStore = new ConcurrentHashMap<>();

    @Tool(
            name = "save_to_wishlist",
            description = "Save a product title to the user's wishlist (in-memory)."
    )
    public String saveToWishlist(
            @ToolParam(description = "Username of the user") String username,
            @ToolParam(description = "Exact product title to store") String productTitle
    ) {
        wishlistStore.computeIfAbsent(username, k -> new ArrayList<>()).add(productTitle);
        return "Saved: " + productTitle;
    }

    @Tool(
            name = "get_wishlist",
            description = "Get the user's wishlist (in-memory)."
    )
    public List<String> getWishlist(
            @ToolParam(description = "Username of the user") String username
    ) {
        return wishlistStore.getOrDefault(username, List.of());
    }
}
