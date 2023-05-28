package com.orzelke.authservice.error;

public class RegistrationException extends RuntimeException{
    public RegistrationException(String message) {
        super(message);
    }
}
