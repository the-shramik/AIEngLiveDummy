package com.telusko.config;

import com.telusko.tools.DateTimeTool;
import com.telusko.tools.NewsTool;
import org.springframework.ai.support.ToolCallbacks;
import org.springframework.ai.tool.ToolCallback;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;

@Configuration
public class McpServerConfig {

    @Bean
    List<ToolCallback> toolCallbacks(DateTimeTool dateTimeTool, NewsTool newsTool) {
        return List.of(ToolCallbacks.from(dateTimeTool,newsTool));
    }
}
