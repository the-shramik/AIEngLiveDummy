package com.telusko.tools;

import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.context.i18n.LocaleContextHolder;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.ZoneId;

@Component
public class DateTimeTools {

    @Tool(name = "getCurrentLocalTime",description = "Get the current date and time in the user's timezone.")
    public String getCurrentLocalTime() {
        return LocalDateTime.now().toString();
    }

    @Tool(name = "getCurrentTime",
            description = "Get the current time in the specified time zone.")
    public String getCurrentTime(@ToolParam(
            description = "Value representing the time zone") String timeZone){

        return LocalTime.now(ZoneId.of(timeZone)).toString();
    }
}
