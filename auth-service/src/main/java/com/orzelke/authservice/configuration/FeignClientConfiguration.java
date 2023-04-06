package com.orzelke.authservice.configuration;

import com.orzelke.authservice.error.FaceRecognitionErrorDecoder;
import org.springframework.context.annotation.Bean;

public class FeignClientConfiguration {
    @Bean
    public FaceRecognitionErrorDecoder faceRecognitionErrorDecoder() {
        return new FaceRecognitionErrorDecoder();
    }
}
