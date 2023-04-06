package com.orzelke.authservice.error;

public class UnknownException extends RuntimeException {
    public UnknownException(String message) {
        super(message);
    }
}
