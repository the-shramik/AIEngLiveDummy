package com.telusko.config;
import org.springframework.ai.embedding.EmbeddingModel;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.ai.vectorstore.mariadb.MariaDBVectorStore;
import org.springframework.ai.vectorstore.mariadb.MariaDBVectorStore.MariaDBDistanceType;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.jdbc.core.JdbcTemplate;

@Configuration
public class AppConfig {

    @Bean
    public VectorStore vectorStore(JdbcTemplate jdbcTemplate, EmbeddingModel embeddingModel) {

        return MariaDBVectorStore.builder(jdbcTemplate, embeddingModel)
                .vectorTableName("vector_store")
                .dimensions(1536)
                .distanceType(MariaDBDistanceType.COSINE)
                .initializeSchema(true)

                .build();
    }
}
