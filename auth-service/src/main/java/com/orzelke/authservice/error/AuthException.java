package com.orzelke.authservice.error;

public class AuthException extends RuntimeException{
    public AuthException() {
        super("Bad credentials or face not recognized.");
    }
}
