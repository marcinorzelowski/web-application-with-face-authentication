package com.orzelke.authservice.error;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.orzelke.authservice.dto.ExceptionResponse;
import feign.FeignException;
import feign.Response;
import feign.codec.ErrorDecoder;

import java.io.IOException;
import java.io.InputStream;

public class FaceRecognitionErrorDecoder implements ErrorDecoder {

    private final ErrorDecoder errorDecoder = new Default();
    @Override
    public Exception decode(String methodKey, Response response) {

        ExceptionResponse message = null;
        try (InputStream bodyIs = response.body().asInputStream()) {
            ObjectMapper mapper = new ObjectMapper();
            message = mapper.readValue(bodyIs, ExceptionResponse.class);
        } catch (IOException e) {
            return new Exception(e.getMessage());
        }
        return switch (response.status()) {
            case 400 -> new IncorrectNumberOfFacesException(message.getError() != null ? message.getError() : "Bad Request");
            case 500 -> new UnknownException(message.getError() != null ? message.getError() : "Unknown Exception.");
            default -> errorDecoder.decode(methodKey, response);
        };
    }

}
