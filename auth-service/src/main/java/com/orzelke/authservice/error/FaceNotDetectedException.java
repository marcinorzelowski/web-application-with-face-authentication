package com.orzelke.authservice.error;

public class FaceNotDetectedException extends RuntimeException{
    public FaceNotDetectedException(String message) {
        super(message);
    }
}
