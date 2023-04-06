package com.orzelke.authservice.error;

public class IncorrectNumberOfFacesException extends RuntimeException{
    public IncorrectNumberOfFacesException(String message) {
        super(message);
    }
}
